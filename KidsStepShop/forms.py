from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Footwear


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        help_text=_('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы'),
        widget=forms.TextInput(attrs={'placeholder': _('Логин')}))
    first_name = forms.CharField(help_text=_('Обязательное поле.'), widget=forms.TextInput(attrs={'placeholder': _('Имя')}))
    last_name = forms.CharField(help_text=_('Обязательное поле.'),
                                widget=forms.TextInput(attrs={'placeholder': _('Фамилия')}))
    phone = forms.CharField(help_text=_('Формат 000-0000000.'), widget=forms.TextInput(attrs={'placeholder': _('Телефон')}))
    email = forms.EmailField(help_text=_('Обязательное поле.'), widget=forms.EmailInput(attrs={'placeholder': _('Эл. почта')}))
    password1 = forms.CharField(help_text=_('Минимум 8 символов. Пароль не может состоять только из цифр.'),
                                widget=forms.PasswordInput(attrs={'placeholder': _('Пароль')}))
    password2 = forms.CharField(help_text=_('Для подтверждения введите, пожалуйста, пароль ещё раз.'),
                                widget=forms.PasswordInput(attrs={'placeholder': _('Подтвердите пароль')}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2',)


class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Логин')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Пароль')}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(help_text=_('Введите e-mail который был указан при регистрации.'),
                             widget=forms.EmailInput(attrs={'placeholder': _('Эл. почта')}))




