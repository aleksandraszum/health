from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from healthsite.forms import SignUpForm, LoginForm


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
            return render(request, 'healthsite/successfulregistration.html', {'comunicate': communicate, 'login': False})
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
                        return render(request, 'healthsite/login.html', {'form': form, 'communicate': communicate, 'login': False})
                else:
                    communicate = "Login or password are incorrect."
                    return render(request, 'healthsite/login.html', {'form': form, 'communicate': communicate, 'login': False})
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