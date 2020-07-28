from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Username:")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password:")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat the password:")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
