from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RegistrationPageView, AuthorizationPageView

urlpatterns = [
    path('register/', RegistrationPageView.as_view(), name='register'),
    path('login/', AuthorizationPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
