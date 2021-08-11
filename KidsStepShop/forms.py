from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Footwear


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    first_name = forms.CharField(help_text='Обязательное поле.', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(help_text='Обязательное поле.',
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    phone = forms.CharField(help_text='Формат 000-0000000.', widget=forms.TextInput(attrs={'placeholder': 'Телефон'}))
    email = forms.EmailField(help_text='Обязательное поле.', widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(help_text='Минимум 8 символов. Пароль не может состоять только из цифр.',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2',)


class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(help_text='Введите e-mail который был указан при регистрации.',
                             widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))




