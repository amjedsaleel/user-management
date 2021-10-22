# django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
                               error_messages={'unique': 'User name is already taken, Please choose another one'})
    first_name = forms.CharField(required=True, max_length=150,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(required=True, max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password1 = forms.CharField(label='Password', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
                                help_text='Password must be alphanumeric, Password must contain at least 8 characters')
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
