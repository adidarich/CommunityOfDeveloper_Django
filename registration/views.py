from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm, SignInForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('registration:signin')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'registration/signin.html'

