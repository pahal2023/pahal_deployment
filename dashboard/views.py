from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .forms import LoginForm

# Create your views here.
def error_page(request):
    return render(request, 'dashboard/error.html')

def login_page(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # At this point, the CAPTCHA has already been successfully validated by ReCaptchaField

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("/")
            else:
                # This block handles invalid username/password combinations
                # without revealing whether the username exists or not.
                # It's better for security to give a generic error.
                messages.error(request, "Invalid username or password.")
        else:
            # If the form is NOT valid, it means either:
            # 1. Username/Password validation failed (e.g., empty fields if required)
            # 2. The CAPTCHA validation failed
            # The form object will contain errors which are displayed in the template.
            # You might want to log these errors for debugging.
            # print(form.errors) # Uncomment for debugging form errors
            pass  # No specific message needed here, errors will show on the form

    else:
        form = LoginForm()

    return render(request, 'dashboard/login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url="/login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/login')
        else:
            messages.error(request, "Input fields are not valid.")
    return render(request, "dashboard/change_password.html")
