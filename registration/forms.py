from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, EmailInput, CharField, EmailField


class SignUpForm(UserCreationForm):
    username = CharField(
        widget=TextInput(
            attrs={
                'name': 'name',
                'id': 'name',
                'placeholder': 'Enter your username'
            }
        )
    )
    password1 = CharField(
        widget=PasswordInput(
            attrs={
                'name': 'pass',
                'id': 'pass',
                'placeholder': 'Enter your password'
            }
        )
    )
    password2 = CharField(
        widget=PasswordInput(
            attrs={
                'name': 're_pass',
                'id': 're_pass',
                'placeholder': 'Confirm your password'
            }
        )
    )
    email = EmailField(
        widget=EmailInput(
            attrs={
                'name': 'email',
                'id': 'email',
                'placeholder': 'Enter your email'
            }
        )
    )


class SignInForm(AuthenticationForm):
    username = UsernameField(
        widget=TextInput(
            attrs={
                'name': 'name',
                'id': 'name',
                'placeholder': 'Enter your username'
            }
        )
    )
    password = CharField(
        widget=PasswordInput(
            attrs={
                'name': 'password',
                'id': 'password',
                'placeholder': 'Enter your password'
            }
        )
    )