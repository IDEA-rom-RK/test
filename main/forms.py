
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        max_length=150,
        help_text="Придумайте уникальный логин.",
        error_messages={
            "required": "Введите логин.",
            "unique": "Этот логин уже занят."
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Ваш логин",
            "autocomplete": "username"
        })
    )

    password1 = forms.CharField(
        label="Пароль",
        help_text="Минимум 8 символов.",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Придумайте пароль",
            "autocomplete": "new-password"
        })
    )

    password2 = forms.CharField(
        label="Повторите пароль",
        help_text="Введите пароль ещё раз для проверки.",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Повторите пароль",
            "autocomplete": "new-password"
        })
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            "placeholder": "Ваш логин",
            "autocomplete": "username"
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Ваш пароль",
            "autocomplete": "current-password"
        })
    )
