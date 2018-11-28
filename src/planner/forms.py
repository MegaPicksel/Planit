from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import DinnerDecider, TodoList
from django.contrib.auth import get_user_model
User = get_user_model()


TIME_CHOICES = ('00:00', '01:00')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class DinnerDeciderForm(forms.ModelForm):

    class Meta:
        model = DinnerDecider
        fields = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


class TodoForm(forms.ModelForm):
    Task = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter a task'}))
    Date = forms.DateTimeField(label='', widget=forms.DateInput(attrs={'id':'datepicker', 'autocomplete':'off',
                                                                   'placeholder': 'Enter a date and time'}))
    Info = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Add aditional info', 
                                                                                'cols':40, 'rows': 8}))
    
    class Meta:
        model = TodoList
        fields = ('Task', 'Date', 'Info')


class WeatherForm(forms.Form):
    City = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter a city'}))

    class Meta:
        fields = ('City',)


class ContactForm(forms.Form):
    Name = forms.CharField(label='')
    Message = forms.CharField(label='', widget=forms.Textarea(attrs={'cols':40, 'rows': 8}))
    Email = forms.CharField(label='')
    user = User

    class Meta:
        fields = ('Name', 'Message', 'Email')


