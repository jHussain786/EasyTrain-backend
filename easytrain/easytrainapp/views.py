from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PersonalaiKeys, Profiles
from django.http import JsonResponse
from integrations.personalai import Personalai
from Crawlers.wrapper import wrapper
import environ
import os
env = environ.Env()
environ.Env.read_env()


def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():

            personalkey = request.POST['personal']
            validate_key = Personalai.validate_key(personalkey)

            if validate_key == False:
                return JsonResponse({"error_message": "Invalid key"})
            
            instance = form.save()

            username = form.cleaned_data.get('username')
            email = request.POST['email']
            
            
            Profiles.objects.create(name=username, email=email, 
                                    PersonalaiKey=personalkey, 
                                    user= instance.id)
            

            return render(request, 'login_user')  # Redirect to the login_user view
            # return JsonResponse({"message": "Account created successfully"})
        else:
            return render(request, 'register_user.html', {"form": form})
            # return JsonResponse({"error_message": "Invalid form data", "message": form.errors})
    return render(request, 'register_user.html')
    # return JsonResponse({"form": form})

def login_user(request):  
    if request.method == 'POST':
        authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('home')  # Redirect to the home view
            # return JsonResponse({"message": "Logged in successfully"})
        else:
            return render(request, 'login_user.html', {"user": authenticated_user})
            # return JsonResponse({"error_message": "Invalid username or password"})
    return render(request, 'login_user.html')
    # return JsonResponse({})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_user')  # Redirect to the login_user view
        # return JsonResponse({"message": "You are logged out"})
    else:
        return render(request, 'login_user.html')
        # return JsonResponse({"message": "You are logged out"})

def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            keyword = request.POST.get('keyword')

            Wrapper = wrapper(keyword, request.user)
            redirect_page = Wrapper.make_payment()
            return redirect(redirect_page)
            return JsonResponse({"redirect_url": redirect_page})
        
        return render(request, 'home.html')
        # return JsonResponse({"key_available": key_available})
    else:
        return redirect('login_user')  # Redirect to the login_user view
        # return JsonResponse({"error_message": "You are not logged in"})

def payment_success(request):
    return JsonResponse({"message": "Payment successful"})

def payment_failed(request):
    return JsonResponse({"message": "Payment failed"})

def get_all_users(request):
    users = Profiles.objects.values('name', 'email', 'PersonalaiKey')
    json = []

    for user in users:
        json.append(user)
    
    return JsonResponse({"users": json})

def get_all_packages(request):
    packages = Packages.objects.values('name', 'description', 'price')
    json = []

    for package in packages:
        json.append(package)
    
    return JsonResponse({"packages": json})

