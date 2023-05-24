from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PersonalaiKeys
from django.http import JsonResponse
from integrations.personalai import Personalai
from Crawlers import wrapper
import environ
env = environ.Env()
environ.Env.read_env()



def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Account created successfully"})
        else:
            return JsonResponse({"error_message": "Invalid form data", "message": form.errors})
    return JsonResponse({"form": form})

def login_user(request):  
    if request.method == 'POST':
        authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(authenticated_user)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return JsonResponse({"message": "Logged in successfully"})
        else:
            return JsonResponse({"error_message": "Invalid username or password"})
    return JsonResponse({})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "You are logged out"})
    else:
        return JsonResponse({"message": "You are logged out"})
            


@login_required(login_url='login_user')
def home(request):
    if request.user.is_authenticated:
        current_user = request.user

        key_available = PersonalaiKeys.objects.filter(user=current_user.id).exists()

        if request.method == 'POST':
            keyword = request.POST.get('keyword')
            ai_key = request.POST.get('key')
            
            if key_available == False:
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

            return JsonResponse({"IDs on PersonalAI": response, "key_available": key_available})
        
        return JsonResponse({"key_available": key_available})
    else:
        return JsonResponse({"error_message": "You are not logged in"})

