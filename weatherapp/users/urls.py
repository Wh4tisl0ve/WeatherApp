from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegistrationView, AuthorizationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', AuthorizationView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
