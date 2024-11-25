from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login

from .forms import UserCreationForm, UserAuthorizationForm


class RegistrationPageView(TemplateView):
    template_name = "users/register.html"

    def get(self, request):
        register_form = UserCreationForm()
        return render(request, self.template_name, {"form": register_form})

    def post(self, request):
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.save()
            return redirect("users:login")

        return render(request, self.template_name, {"form": register_form})


class AuthorizationPageView(TemplateView):
    template_name = "users/login.html"

    def get(self, request):
        auto_form = UserAuthorizationForm()
        return render(request, self.template_name, {"form": auto_form})

    def post(self, request):
        auto_form = UserAuthorizationForm(request.POST)

        if auto_form.is_valid():
            username = auto_form.cleaned_data["username"]
            password = auto_form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("weather:main")

        return render(request, self.template_name, {"form": auto_form})
