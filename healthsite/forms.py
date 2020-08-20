from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from healthsite.models import MealPlan, Exercise, Profile


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


class AddExercisePlanForm(forms.ModelForm):
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError(message='Date cannot be in the past')
        return date

    class Meta:
        model = Exercise
        fields = ('date', 'exercise', 'movie')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'exercise': forms.TextInput(attrs={'size': '50'}),
            'movie': forms.TextInput(attrs={'size': '50'}),
        }


class EditExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('exercise', 'movie')
        widgets = {
            'exercise': forms.TextInput(attrs={'size': '50'}),
            'movie': forms.TextInput(attrs={'size': '50'}),
        }


class ProfileForm(forms.ModelForm):
    actual_weight = forms.FloatField(min_value=0)
    dream_weight = forms.FloatField(min_value=0)
    height = forms.IntegerField(min_value=0)
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'date_of_birth', 'height', 'actual_weight', 'dream_weight')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
