import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.datetime_safe import strftime

from healthsite.forms import SignUpForm, LoginForm, AddMealForm, EditMealForm, AddExercisePlanForm, EditExerciseForm, \
    ProfileForm
from healthsite.models import MealPlan, Exercise, Profile


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
            print(User(pk=user.pk).pk)
            profile = Profile(user=User(pk=user.pk))
            profile.save()
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
        except MealPlan.DoesNotExist:
            yesterday_meal = False

        try:
            tomorrow_meal = MealPlan.objects.get(user=user, date=tomorrow)
        except MealPlan.DoesNotExist:
            tomorrow_meal = False

        return render(request, 'healthsite/showmeal.html',
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

        return render(request, 'healthsite/showpreviousmeal.html',
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

        return render(request, 'healthsite/showfuturemeal.html',
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

        return render(request, 'healthsite/showtodaymeal.html',
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
                try:
                    meals = MealPlan.objects.get(user=User(pk=user), date=date)
                    unique_error = "User and date is already exist."
                    return render(request, 'healthsite/addmeal.html',
                                  {'form': form, 'login': True, 'error': unique_error})

                except MealPlan.DoesNotExist:
                    meals = False

                breakfast = str(form['breakfast'].value())
                lunch = str(form['lunch'].value())
                dinner = str(form['dinner'].value())
                supper = str(form['supper'].value())
                meal = MealPlan(user=User(pk=user), date=date, breakfast=breakfast, lunch=lunch, dinner=dinner,
                                supper=supper)
                meal.save()
                return render(request, 'healthsite/successfuladdmeal.html', {"login": True, 'date': date})
            date_error = "Date cannot be in the past"
            form = AddMealForm()
            return render(request, 'healthsite/addmeal.html', {'form': form, 'login': True, 'error': date_error})
        form = AddMealForm()
        return render(request, 'healthsite/addmeal.html', {'form': form, 'login': True})

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
        return render(request, 'healthsite/edit.html', {'login': True, 'meals': meals})
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

            return render(request, 'healthsite/editmealsuccessfully.html',
                          {'form': form, 'login': True, 'day': meals})
        form = EditMealForm(instance=meals)
        return render(request, 'healthsite/editmeal.html', {'form': form, 'login': True, 'day': meals})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_exercise_plan(request):
    if request.user.is_authenticated:
        user = request.user
        date = datetime.date.today()
        try:
            exercise = Exercise.objects.get(user=user, date=date)
        except Exercise.DoesNotExist:
            exercise = False

        return render(request, 'healthsite/showexercise.html',
                      {'user': user, 'login': True, 'exercise': exercise, 'date': date})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_previous_or_next_exercise_plan(request, option, day, month, year):
    if request.user.is_authenticated:
        user = request.user
        year = 2000 + int(year)
        date = datetime.date(year, int(month), int(day))

        if int(option) == 1:
            date = date - datetime.timedelta(days=1)
        else:
            date = date + datetime.timedelta(days=1)

        try:
            exercise = Exercise.objects.get(user=user, date=date)
        except Exercise.DoesNotExist:
            exercise = False
        return render(request, 'healthsite/showexercise.html',
                      {'user': user, 'login': True, 'exercise': exercise, 'date': date})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_today_exercise_plan(request):
    if request.user.is_authenticated:
        user = request.user
        date = datetime.date.today()
        try:
            exercise = Exercise.objects.get(user=user, date=date)
        except Exercise.DoesNotExist:
            exercise = False

        return render(request, 'healthsite/showtodayxercise.html',
                      {'user': user, 'login': True, 'exercise': exercise, 'date': date})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def show_future_exercise_plan(request):
    if request.user.is_authenticated:
        user = request.user
        date_1 = datetime.date.today()
        date_2 = datetime.date.today() + datetime.timedelta(days=1)
        date_3 = datetime.date.today() + datetime.timedelta(days=2)
        date_4 = datetime.date.today() + datetime.timedelta(days=3)
        date_5 = datetime.date.today() + datetime.timedelta(days=4)
        date_6 = datetime.date.today() + datetime.timedelta(days=5)
        date_7 = datetime.date.today() + datetime.timedelta(days=6)

        try:
            exercise_1 = Exercise.objects.get(user=user, date=date_1)
        except Exercise.DoesNotExist:
            exercise_1 = False

        try:
            exercise_2 = Exercise.objects.get(user=user, date=date_2)
        except Exercise.DoesNotExist:
            exercise_2 = False

        try:
            exercise_3 = Exercise.objects.get(user=user, date=date_3)
        except Exercise.DoesNotExist:
            exercise_3 = False

        try:
            exercise_4 = Exercise.objects.get(user=user, date=date_4)
        except Exercise.DoesNotExist:
            exercise_4 = False

        try:
            exercise_5 = Exercise.objects.get(user=user, date=date_5)
        except Exercise.DoesNotExist:
            exercise_5 = False

        try:
            exercise_6 = Exercise.objects.get(user=user, date=date_6)
        except Exercise.DoesNotExist:
            exercise_6 = False

        try:
            exercise_7 = Exercise.objects.get(user=user, date=date_7)
        except Exercise.DoesNotExist:
            exercise_7 = False

        return render(request, 'healthsite/showfuturexercise.html',
                      {'user': user, 'login': True, 'exercise_1': exercise_1, 'date_1': date_1,
                       'exercise_2': exercise_2, 'date_2': date_2, 'exercise_3': exercise_3, 'date_3': date_3,
                       'exercise_4': exercise_4, 'date_4': date_4, 'exercise_5': exercise_5, 'date_5': date_5,
                       'exercise_6': exercise_6, 'date_6': date_6, 'exercise_7': exercise_7, 'date_7': date_7})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def add_exercise(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddExercisePlanForm(request.POST)
            if form.is_valid():
                date = form['date'].value()
                try:
                    exercise = Exercise.objects.get(user=User(pk=request.user.id), date=date)
                    unique_error = "User and date is already exist."
                    return render(request, 'healthsite/addexercise.html',
                                  {'form': form, 'login': True, 'error': unique_error})

                except Exercise.DoesNotExist:
                    exercise = False

                exercise = str(form['exercise'].value())
                movie = str(form['movie'].value())
                exercise = Exercise(user=User(pk=request.user.id), date=date, exercise=exercise, movie=movie)
                exercise.save()
                communicate = "You add exercise plan successfully."
                return render(request, 'healthsite/successful.html',
                              {"login": True, 'communicate': communicate})
            date_error = "Date cannot be in the past"
            form = AddExercisePlanForm()
            return render(request, 'healthsite/addexercise.html', {'form': form, 'login': True, 'error': date_error})
        form = AddExercisePlanForm()
        return render(request, 'healthsite/addexercise.html', {'form': form, 'login': True})

    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def edit_exercise(request):
    if request.user.is_authenticated:
        try:
            exercises = Exercise.objects.filter(user=request.user.id).exclude(
                date__lt=datetime.date.today())
        except Exercise.DoesNotExist:
            exercises = False
        return render(request, 'healthsite/editexercise.html', {'login': True, 'exercises': exercises})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def exercise_edit_pk(request, exercise_id):
    if request.user.is_authenticated:
        exercise = Exercise.objects.get(pk=exercise_id)
        if request.method == 'POST':
            form = EditExerciseForm(request.POST, instance=exercise)
            if form.is_valid():
                plan = form.save(commit=False)
                plan.user = User(pk=request.user.id)
                plan.pk = exercise_id
                plan.save()
            communicate = "Edit plan successfully."
            return render(request, 'healthsite/successful.html',
                          {'login': True, 'communicate': communicate})
        form = EditExerciseForm(instance=exercise)
        return render(request, 'healthsite/editexercisepk.html', {'form': form, 'login': True})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def profile(request):
    if request.user.is_authenticated:
        user = request.user.id
        profile = Profile.objects.get(user=user)
        if profile.date_of_birth is not True:
            now = datetime.datetime.now()
            age = now.year - profile.date_of_birth.year
        else:
            age = "No data"
        return render(request, 'healthsite/profile.html', {'login': True, 'profile': profile, 'age': age})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})


def profile_edit(request):
    if request.user.is_authenticated:
        user = request.user.id
        profile = Profile.objects.get(user=user)
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                profile_data = form.save(commit=False)
                profile_data.user = User(pk=user)
                profile_data.pk = profile.id
                profile_data.save()
        form = ProfileForm(instance=profile)
        print("yolo 2")
        return render(request, 'healthsite/profileedit.html', {'login': True, 'profile': profile, 'form': form})
    else:
        return render(request, 'healthsite/homepage.html', {'login': False})
