from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from healthsite.models import MealPlan, Exercise, Profile, EatingHabit


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


class EatingHabitsForm(forms.ModelForm):
    class Meta:
        model = EatingHabit
        fields = ('habits1', 'habits2', 'habits3')
        widgets = {
            'habits1': forms.TextInput(attrs={'size': '50'}),
            'habits2': forms.TextInput(attrs={'size': '50'}),
            'habits3': forms.TextInput(attrs={'size': '50'}),
        }


class EatingHabitsCheckForm(forms.ModelForm):
    class Meta:
        model = EatingHabit
        fields = (
            'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11', 'day12', 'day13',
            'day14', 'day15', 'day16', 'day17', 'day18', 'day19', 'day20', 'day21')
        widgets = {
            'day1': forms.CheckboxInput,
            'day2': forms.CheckboxInput,
            'day3': forms.CheckboxInput,
            'day4': forms.CheckboxInput,
            'day5': forms.CheckboxInput,
            'day6': forms.CheckboxInput,
            'day7': forms.CheckboxInput,
            'day8': forms.CheckboxInput,
            'day9': forms.CheckboxInput,
            'day10': forms.CheckboxInput,
            'day11': forms.CheckboxInput,
            'day12': forms.CheckboxInput,
            'day13': forms.CheckboxInput,
            'day14': forms.CheckboxInput,
            'day15': forms.CheckboxInput,
            'day16': forms.CheckboxInput,
            'day17': forms.CheckboxInput,
            'day18': forms.CheckboxInput,
            'day19': forms.CheckboxInput,
            'day20': forms.CheckboxInput,
            'day21': forms.CheckboxInput,
        }
