from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя",max_length=120)
    email = forms.EmailField(label="Почта",max_length=150)
    password1 = forms.CharField(label="Пароль",max_length=80,strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    password2 = forms.CharField(label="Подтверждение пароля",max_length=80,strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLogInForm(AuthenticationForm):
    username = forms.CharField(max_length=120, label="Имя")
    password = forms.CharField(max_length=120, label="Пароль",strip=False,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),)

