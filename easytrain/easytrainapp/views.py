from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Profiles, Packages
from django.http import JsonResponse
from integrations.personalai import Personalai
from integrations.weather import WeatherData
from Crawlers.wrapper import wrapper



@csrf_exempt
@api_view(['POST'])
def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            
            personalkey = request.POST['personal']
            validate_key = Personalai(personalkey).validate_key()

            if validate_key == False:
                return JsonResponse({"error_message": "Invalid key"})
            
            instance = form.save()

            username = form.cleaned_data.get('username')
            email = request.POST['email']
            
            
            Profiles.objects.create(name=username, email=email, 
                                    PersonalaiKey=personalkey, 
                                    user= instance.id)
            
            return JsonResponse({"message": "Account created successfully"})

        else:
            return JsonResponse({"error_message": "Invalid form data", "message": form.errors})
    return JsonResponse({"form": form})

@csrf_exempt
@permission_classes([IsAuthenticated])
def login_user(request):  
    authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if authenticated_user is not None:
        login(request, authenticated_user)
        return JsonResponse({"message": "Logged in successfully"})
    else:
        return JsonResponse({"error_message": "Invalid username or password"})

@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "You are logged out"})

@csrf_exempt
@permission_classes([IsAuthenticated])
def home(request):
    keyword = request.POST.get('keyword')
    Wrapper = wrapper(keyword, request.user)
    redirect_page = Wrapper.make_payment()
    return JsonResponse({"redirect_url": redirect_page})

def payment_success(request):
    user_package = Packages.objects.filter(user=request.user.id).last()

    user_package.is_active = True
    user_package.save()

    key = Profiles.objects.get(user=request.user.id).PersonalaiKey
    personalai = Personalai(key)

    print("urls: ", user_package.urls)

    personalai.upload(user_package.urls.split(" "))
    
    return JsonResponse({"message": "Payment successful and urls uploaded to personalai"})

def payment_failed(request):
    return JsonResponse({"message": "Payment failed and url upload to personalai failed"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = Profiles.objects.values('name', 'email', 'PersonalaiKey')
    json = []
    for user in users:
        json.append(user)
    return JsonResponse({"users": json})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_packages(request):
    packages = Packages.objects.values('name', 'updated_time', 'urls', 'price')
    json = []

    for package in packages:
        json.append(package)
    
    return JsonResponse({"packages": json})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather(request):
    personalkey = Profiles.objects.get(user=request.user.id).PersonalaiKey
    weather_data = WeatherData(personalkey).get_weather_data_by_city_name('London')
    return JsonResponse({"message": "Weather data uploaded to personalai", "weather_data": weather_data})

def health(request):
    return JsonResponse({"message": "Server is up and running"})