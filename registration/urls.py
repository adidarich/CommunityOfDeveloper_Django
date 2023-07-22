from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import SignUpView, SignInView, ProfileView

app_name = 'registration'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/profile', ProfileView.as_view(), name='profile'),
]
