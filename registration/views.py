from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View

from .forms import SignUpForm, SignInForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('registration:signin')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'registration/signin.html'
    success_url = reverse_lazy('cd:list')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'registration/profile.html'
    login_url = '/signin/'

    def get(self, request: HttpRequest) -> HttpResponse:
        user = User.objects.filter(username=request.user)[0]
        return render(request, self.template_name, {'user': user})
