import self as self
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import *
from django.contrib.auth.models import User


class LogForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'тебя {username} нет')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('проебка в пароле')
        return self.cleaned_data


class CreatUserForm(forms.ModelForm):
    username = forms.CharField(label='ЛОГИН', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    password1 = forms.CharField(label='ПАРОЛЬ1', widget=forms.PasswordInput(attrs={'class': 'form-input'}),
                                required=True)
    password2 = forms.CharField(label='ПАРОЛЬ2', widget=forms.PasswordInput(attrs={'class': 'form-input'}),
                                required=True)
    email = forms.EmailField(label='ПОЧТА', widget=forms.EmailInput(attrs={'class': 'form-input'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'date_joined']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

