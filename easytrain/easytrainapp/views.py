from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PersonalaiKeys, Profiles
from django.http import JsonResponse
from integrations.personalai import Personalai
from Crawlers import wrapper
import environ
import os
env = environ.Env()
environ.Env.read_env()

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = request.POST['email']
            personalkey = request.POST['personal']

            Profiles.objects.create(name=username, email=email, PersonalaiKey=personalkey, user=1)

            return render('login_user')  # Redirect to the login_user view
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

        key_available = PersonalaiKeys.objects.filter(user=current_user.id).exists()

        if request.method == 'POST':
            keyword = request.POST.get('keyword')
            ai_key = request.POST.get('key')
            
            if not key_available:
                if Personalai(key=ai_key).validate_key():
                    ai_key_obj = PersonalaiKeys(key=ai_key, user=current_user.id)
                    ai_key_obj.save()
                    key_available = True
                else:
                    return JsonResponse({"error_message": "Invalid key"}) 
            else:
                ai_key = PersonalaiKeys.objects.get(user=current_user.id).key

            response = wrapper.get_urls(keyword)
            per_ai = Personalai(ai_key)
            response = per_ai.upload(response)

            return render(request, 'home.html', {"IDs on PersonalAI": response, "key_available": key_available})
            # return JsonResponse({"IDs on PersonalAI": response, "key_available": key_available})
        
        return render(request, 'home.html', {"key_available": key_available})
        # return JsonResponse({"key_available": key_available})
    else:
        return redirect('login_user')  # Redirect to the login_user view
        # return JsonResponse({"error_message": "You are not logged in"})


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