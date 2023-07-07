from django.urls import path, include
from .views import SignUpView, SignInView

app_name = 'registration'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    # path('logout/', name='signin'),
    # path('account/profile', name='signin'),
]