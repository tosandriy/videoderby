from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import  Profile
from django.forms.widgets import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'a'
    input_text = 'b'
    clear_checkbox_label = 'c'

    def get_context(self, name, value, attrs) :
        context = super().get_context(name, value, attrs)
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)
        context['widget'].update({
                'checkbox_name' : checkbox_name,
                'checkbox_id' : checkbox_id,
                'is_initial' : False,
                'input_text' : self.input_text,
                'initial_text' : self.initial_text,
                'clear_checkbox_label' : self.clear_checkbox_label,
        })
        return context


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя",max_length=120)
    email = forms.EmailField(label="Почта",max_length=150)
    password1 = forms.CharField(label="Пароль",max_length=80,strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    password2 = forms.CharField(label="Подтверждение пароля",max_length=80,strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    def clean_email(self) :
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists() :
            raise forms.ValidationError(u'Уже существует аккаунт с такой почтой.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class UserLogInForm(AuthenticationForm):
    username = forms.CharField(max_length=120, label="Имя")
    password = forms.CharField(max_length=120, label="Пароль",strip=False,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),)


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label="Текущее Имя")
    email = forms.EmailField(label="Почта")

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    picture = forms.ImageField(label='Аватар', required=False, widget=MyClearableFileInput)

    class Meta:
        model = Profile
        fields = ['picture']