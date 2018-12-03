import requests
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout, get_user_model
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.template.loader import render_to_string
from users.admin import UserCreationForm, UserChangeForm
from .models import DinnerDecider, TodoList
from users.models import UserProfile
from .forms import LoginForm, DinnerDeciderForm, TodoForm, WeatherForm, ContactForm
from .tasks import plan_email, contact_email


class LoginMixin(LoginRequiredMixin):
    """ Any View that requires Login to be accessed inherits from this mixin."""
    login_url = '/'
    redirect_field_name = 'login'


class LandingView(TemplateView):
    template_name = 'users/landing.html'


class SignUpView(SuccessMessageMixin, CreateView):
    """ Note that the UserCreationForm comes from the custom user model."""
    template_name = 'users/registration.html'
    form_class = UserCreationForm
    success_url = 'login'
    success_message = 'Thank you for signing up, please login.'


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/home/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')


class HomeView(LoginMixin, TemplateView):
    template_name = 'planner/home.html'
    
    def get_context_data(self, **kwargs):
        context = {
            'todo_form': TodoForm,
            'user': self.request.user,
            'dinner_plan': DinnerDecider.objects.filter(User=self.request.user).order_by('-Timestamp')[:1],
            'todo_list': TodoList.objects.filter(User=self.request.user).order_by('Date'),
        }
        return context


class TodayAjaxView(LoginMixin, TemplateView):
    """ 
    Creates the section that displays todays appointments, because the ajax call for this view happens
    on page load, HomeView does not need a queryset for this feature.
    """
    template_name = 'planner/today.html'

    def get(self, request):
        """ 
        date variable must be set each time the view is called, if set as a class attribute it gets set once
        causing the wrong date to be set for every day past the day that this script is first run on the server.
        """
        data = dict()
        date = datetime.date.today()                
        today=TodoList.objects.filter(User=self.request.user).filter(Date__date=date)
        data['html_data'] = render_to_string(self.template_name, {'today': today})     
        return JsonResponse(data)


class DinnerPlanMixin(LoginMixin):
    form_class = DinnerDeciderForm
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.User = self.request.user
        user = str(self.request.user)
        monday = form.cleaned_data['Monday']
        tuesday = form.cleaned_data['Tuesday']
        wednesday = form.cleaned_data['Wednesday']
        thursday = form.cleaned_data['Thursday']
        friday = form.cleaned_data['Friday']
        saturday = form.cleaned_data['Saturday']
        sunday = form.cleaned_data['Sunday']
        try:
            plan_email.delay(monday, tuesday, wednesday, thursday, friday, saturday, sunday, user)
            messages.success(self.request, "Your dinner plan hasa been emailed to you.")
        except Exception:
            messages.error(self.request, "An error occured when emailing you a copy of your dinner plan.")
        return super().form_valid(form) 


class DinnerPlanView(DinnerPlanMixin, CreateView):
    """ An email will be sent, via Celery, to the users email when they create a new dinner plan."""
    template_name = 'planner/decider.html'


class DinnerPlanUpdateView(DinnerPlanMixin, UpdateView):
    """ Update an item in the dinner plan. """
    template_name = 'planner/decider_update.html'
    model = DinnerDecider

    def get_object(self): 
        return get_object_or_404(DinnerDecider, pk=self.kwargs["pk"])


class AjaxTodoView(LoginMixin, CreateView):
    """ Create a task, this view responds to an ajax call. 
    The view supplies a form (displayed in a modal, hence the get method), 
    and submits it if valid, otherwise the javascript will display an alert informing 
    the user of the error. """
    form_class = TodoForm

    def get(self, form):
        data = dict()
        self.form = TodoForm
        data['html_data'] = render_to_string('planner/todo_form.html', {'todo_form': self.form}, request=self.request)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['operation_is_valid'] = False
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()
        form.instance.User = self.request.user
        form.save()
        todo_list = TodoList.objects.filter(User=self.request.user).order_by('Date')
        data['operation_is_valid'] = True
        data['html_data'] = render_to_string('planner/todo_list.html', {'todo_list': todo_list})
        return JsonResponse(data)


class AjaxTodoUpdateView(LoginMixin, UpdateView):
    """ Update a task in the todo list."""
    model = TodoList

    def get(self, request, *args, **kwargs):
        data = dict()
        self.form = TodoForm(instance=get_object_or_404(TodoList, pk=self.kwargs['pk']))
        data['html_data'] = render_to_string('planner/todolist_update.html', {'todo_form': self.form}, request=self.request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = dict()
        form = TodoForm(request.POST, instance=get_object_or_404(TodoList, pk=self.kwargs['pk']))
        form.save()
        todo_list = TodoList.objects.filter(User=request.user).order_by('Date')
        data['operation_is_valid'] = True
        data['html_data'] = render_to_string('planner/todo_list.html', {'todo_list': todo_list})
        return JsonResponse(data)


class TodoDeleteMixin(LoginMixin):

    def get(self, request, *args, **kwargs):
        data = dict()
        self.todo = get_object_or_404(TodoList, pk=self.kwargs['pk'])
        data['html_data'] = render_to_string(self.template_name, {'todo':self.todo}, request=self.request)
        return JsonResponse(data)

class AjaxTodoInfoView(TodoDeleteMixin, View):
    """ Display extra information about a specific task in the todo list."""
    template_name = 'planner/todo_info.html'


class AjaxTodoDeleteView(TodoDeleteMixin, DeleteView):
    """ Delete a task from todo list, this view displays a 'confrim delete' modal, 
    if it is submitted, the corresponding object is deleted."""
    template_name = 'planner/todo_delete.html'

    def post(self, request, *args, **kwargs):
        data = dict()
        todo = get_object_or_404(TodoList, pk=self.kwargs['pk'])
        todo.delete()
        todo_list = TodoList.objects.filter(User=request.user).order_by('Date')
        data['operation_is_valid'] = True
        data['html_data'] = render_to_string('planner/todo_list.html', {'todo_list': todo_list})
        return JsonResponse(data)     


class AjaxWeatherView(LoginMixin, TemplateView):
    """FormView requires a template_name due to its inheritance from classes higher up in the inheritance tree."""
    template_name = 'planner/home.html'

    def get(self, request):
        city = self.request.user.city
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ea6e9077acfd6b6983f37747aeb230ce'
        r = requests.get(url.format(city)).json()
        data = {
            'city': r['name'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'temp' : r['main']['temp'],
            'humidity' : r['main']['humidity'],
            'wind': r['wind']['speed']
        }
        return JsonResponse(data)


class ContactMixin(FormView):
    form_class = ContactForm
    
    def form_valid(self, form):
        name = form.cleaned_data['Name']
        message = form.cleaned_data['Message']
        email = form.cleaned_data['Email']
        try:
            contact_email.delay(name, message, email)
            messages.success(self.request, "Email sent, we will be in contact shortly.")
        except Exception:
            messages.error(self.request, "An error occured and your email was not sent, please try again.")
        return super().form_valid(form)

class ContactView(LoginMixin, ContactMixin):
    """ Email is sent via celery."""
    template_name = 'planner/contact.html'
    success_url = '/home/'


class ContactLandingView(ContactMixin):
    """ Contact form seen by non-logged in users/non-registered users."""
    template_name = 'users/contact_landing.html'
    success_url = '/'


class AccountView(LoginMixin, TemplateView):
    """ Display account information. """
    template_name = 'planner/account.html'

    def get_context_data(self, **kwargs):
        context = {
            'user': UserProfile.objects.filter(pk=self.request.user.pk)
        }
        return context


class AccountUpdateView(LoginMixin, UpdateView):
    """ Allow users to edit their account information."""
    form_class = UserChangeForm
    model = UserProfile
    success_url = '/home/'
    template_name = 'planner/account_update.html'

    def get_object(self): 
        return get_object_or_404(UserProfile, pk=self.kwargs["pk"])

    def form_valid(self, form):
        return super().form_valid(form)

