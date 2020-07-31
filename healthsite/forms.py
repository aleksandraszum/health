from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from healthsite.models import MealPlan

"""def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError(_("Date cannot be in the past"))
"""


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


class AddMealForm(forms.ModelForm):
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError(message='Date cannot be in the past')
        return date

    class Meta:
        model = MealPlan
        fields = ('date', 'breakfast', 'lunch', 'dinner', 'supper')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'breakfast': forms.TextInput(attrs={'size': '50'}),
            'dinner': forms.TextInput(attrs={'size': '50'}),
            'lunch': forms.TextInput(attrs={'size': '50'}),
            'supper': forms.TextInput(attrs={'size': '50'}),
        }


class EditMealForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ('breakfast', 'lunch', 'dinner', 'supper')
        widgets = {
            'breakfast': forms.TextInput(attrs={'size': '50'}),
            'dinner': forms.TextInput(attrs={'size': '50'}),
            'lunch': forms.TextInput(attrs={'size': '50'}),
            'supper': forms.TextInput(attrs={'size': '50'}),
        }
