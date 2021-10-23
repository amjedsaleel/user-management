# Django
from django.contrib.auth.models import User
from django import forms


class UpdateUser(forms.ModelForm):
    username = forms.CharField(required=True, max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
                               error_messages={'unique': 'User name is already taken, Please choose another one'})
    first_name = forms.CharField(required=True, max_length=150,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(required=True, max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
