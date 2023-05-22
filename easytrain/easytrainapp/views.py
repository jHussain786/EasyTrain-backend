from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

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
            print("Form is valid")
            form.save()
            messages.success(request, 'Account created successfully') 
            return redirect('login')
    return render(request, 'register_user.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if authenticated_user is not None:
            print("Logged in successfully")
            login(request, authenticated_user)
            messages.success(request, 'Logged in successfully') 
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password') 
            return redirect('login')
        
    return render(request, 'login_user.html')

def logout_view(request):
    logout(request)
    return redirect('login_user')

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            keyword = request.POST['keyword']
            response = wrapper.get_urls(keyword)
            per_ai = Personalai(env("PERSONALAI_KEY"))
            
            if per_ai.validate_key():
                response = per_ai.upload(response)
            else:
                return render(request, 'home.html', {"response": "invalid key"})
            return render(request, 'home.html', {"response": response})
    else:
        return redirect('login')
    return render(request, 'home.html')

