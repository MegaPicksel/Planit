from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import DinnerDecider, TodoList
from django.contrib.auth import get_user_model
User = get_user_model()


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
    Due = forms.DateField(label='', widget=forms.DateInput(attrs={'id': 'datepicker', 'autocomplete':'off', 
                                                                  'placeholder': 'Due by'}))
    Info = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Add aditional info'}))

    class Meta:
        model = TodoList
        fields = ('Task', 'Due', 'Info')


class WeatherForm(forms.Form):
    City = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter a city'}))

    class Meta:
        fields = ('City',)


class ContactForm(forms.Form):
    Name = forms.CharField(label='')
    Message = forms.CharField(label='', widget=forms.Textarea())
    Email = forms.CharField(label='')
    user = User

    class Meta:
        fields = ('Name', 'Message', 'Email')


