from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.password_validation import NumericPasswordValidator
from django.utils.translation import gettext_lazy as _

from .validators import validate_latin_and_num
from .models import User


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
        validators=[validate_latin_and_num],
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Введите пароль", "class": "form-control"}
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(20),
            NumericPasswordValidator().validate,
            validate_latin_and_num,
        ],
        error_messages={
            "min_length": _(
                "Пароль должен содержать минимум %(limit_value)d символов (сейчас %(show_value)d)."
            ),
            "max_length": _(
                "Длина пароля не может быть больше %(limit_value)d символов (сейчас %(show_value)d)."
            ),
        },
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Подтвердите пароль", "class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Такой логин уже существует")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли должны совпадать")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAuthorizationForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
        validators=[validate_latin_and_num],
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Введите пароль", "class": "form-control"}
        ),
    )
