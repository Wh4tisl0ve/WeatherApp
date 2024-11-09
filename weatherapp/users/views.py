from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from .forms import UserCreationForm, UserAuthorizationForm


class RegistrationPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        register_form = UserCreationForm()
        return render(request, "users/register.html", {"form": register_form})

    def post(self, request):
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data["password1"])
            new_user.save()
            return redirect(reverse('users:login'))

        return render(request, "users/register.html", {"form": register_form})


class AuthorizationPageView(LoginView):
    authentication_form = UserAuthorizationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = 'main'
