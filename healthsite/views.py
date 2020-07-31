import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.datetime_safe import strftime

from healthsite.forms import SignUpForm, LoginForm, AddMealForm, EditMealForm
from healthsite.models import MealPlan


def index(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'healthsite/indexpage.html', {'user': user, 'login': True})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


# registration
def signup_view(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'healthsite/indexpage.html', {'user': user, 'login': True})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            communicate = "You have successfully registered!"
            return render(request, 'healthsite/successfulregistration.html',
                          {'comunicate': communicate, 'login': False})
        return render(request, 'healthsite/signup.html', {'form': form, 'login': False})


# login
def login_view(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'healthsite/indexpage.html', {'user': user, 'login': True})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                u = form.cleaned_data['username']
                p = form.cleaned_data['password']
                user = authenticate(username=u, password=p)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'healthsite/indexpage.html', {'form': form, 'login': False})
                    else:
                        communicate = "The account has been disabled."
                        return render(request, 'healthsite/login.html',
                                      {'form': form, 'communicate': communicate, 'login': False})
                else:
                    communicate = "Login or password are incorrect."
                    return render(request, 'healthsite/login.html',
                                  {'form': form, 'communicate': communicate, 'login': False})
        else:
            form = LoginForm()
            return render(request, 'healthsite/login.html', {'form': form, 'login': False})


def logout_view(request):
    if request.user.is_authenticated:
        user = request.user
        logout(request)
        communicate = "Successfully logged out!"
        return render(request, 'healthsite/homepage.html', {'communicate': communicate, 'login': False})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_meal_plan(request):
    if request.user.is_authenticated:
        user = request.user
        date = datetime.date.today()
        yesterday = date - datetime.timedelta(days=1)
        tomorrow = date + datetime.timedelta(days=1)
        try:
            today_meal = MealPlan.objects.get(user=user, date=date)
        except MealPlan.DoesNotExist:
            today_meal = False
        try:
            yesterday_meal = MealPlan.objects.get(user=user, date=yesterday)
            print('breakfast:', yesterday_meal.breakfast)
        except MealPlan.DoesNotExist:
            yesterday_meal = False

        try:
            tomorrow_meal = MealPlan.objects.get(user=user, date=tomorrow)
        except MealPlan.DoesNotExist:
            tomorrow_meal = False

        return render(request, 'healthsite/mealplan/showmeal.html',
                      {'user': user, 'login': True, 'today': today_meal, 'yesterday': yesterday_meal,
                       'tomorrow': tomorrow_meal})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_previous_meal_plan(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            meals = MealPlan.objects.filter(user=user).exclude(
                date__gt=datetime.date.today() - datetime.timedelta(days=1))
        except MealPlan.DoesNotExist:
            meals = False

        number = 0
        if meals.count() == 1:
            number = 1
        elif meals.count() == 2:
            number = 2
        else:
            number = 3

        return render(request, 'healthsite/mealplan/showpreviousmeal.html',
                      {'user': user, 'login': True, 'meals': meals, 'number': number})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_future_meal_plan(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            meals = MealPlan.objects.filter(user=user).exclude(
                date__lt=datetime.date.today() + datetime.timedelta(days=1))
        except MealPlan.DoesNotExist:
            meals = False

        number = 0
        if meals.count() == 1:
            number = 1
        elif meals.count() == 2:
            number = 2
        else:
            number = 3

        return render(request, 'healthsite/mealplan/showfuturemeal.html',
                      {'user': user, 'login': True, 'meals': meals, 'number': number})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_today_meal_plan(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            meals = MealPlan.objects.get(user=user, date=datetime.date.today())
        except MealPlan.DoesNotExist:
            meals = False

        return render(request, 'healthsite/mealplan/showtodaymeal.html',
                      {'user': user, 'login': True, 'meals': meals})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def add_meal(request):
    if request.user.is_authenticated:
        user = request.user.id
        if request.method == 'POST':
            form = AddMealForm(request.POST)
            if form.is_valid():
                date = form['date'].value()
                if MealPlan(user=User(pk=user), date=date).DoesNotExist:
                    breakfast = str(form['breakfast'].value())
                    lunch = str(form['lunch'].value())
                    dinner = str(form['dinner'].value())
                    supper = str(form['supper'].value())
                    meal = MealPlan(user=User(pk=user), date=date, breakfast=breakfast, lunch=lunch, dinner=dinner,
                                    supper=supper)
                    meal.save()
                    return render(request, 'healthsite/mealplan/successfuladdmeal.html', {"login": True, 'date': date})
                else:
                    unique_error = "User and date is already exist."
                    return render(request, 'healthsite/mealplan/addmeal.html',
                                  {'form': form, 'login': True, 'unique_error': unique_error})

            return render(request, 'healthsite/mealplan/addmeal.html',
                          {'form': form, 'login': True})
        form = AddMealForm()
        return render(request, 'healthsite/mealplan/addmeal.html', {'form': form, 'login': True})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def meal_edit(request):
    if request.user.is_authenticated:
        user = request.user.id
        try:
            meals = MealPlan.objects.filter(user=user).exclude(
                date__lt=datetime.date.today())
        except MealPlan.DoesNotExist:
            meals = False
        for meal in meals:
            print(meal.date)
        return render(request, 'healthsite/mealplan/edit.html', {'login': True, 'meals': meals})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def meal_edit_pk(request, meal_id):
    if request.user.is_authenticated:
        user = request.user.id
        meals = MealPlan.objects.get(pk=meal_id)
        if request.method == 'POST':
            form = EditMealForm(request.POST, instance=meals)
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = User(pk=user)
                plan.pk = meal_id
                plan.save()

            return render(request, 'healthsite/mealplan/editmealsuccessfully.html',
                          {'form': form, 'login': True, 'day': meals})
        form = EditMealForm(instance=meals)
        return render(request, 'healthsite/mealplan/editmeal.html', {'form': form, 'login': True, 'day': meals})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})
