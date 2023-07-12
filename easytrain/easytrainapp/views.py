import traceback
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.core.serializers import serialize
from datetime import datetime, timedelta
from django.utils import timezone


from .models import Profiles, Packages
from django.http import JsonResponse
from integrations.personalai import Personalai
from integrations.weather import Weather
from integrations.stocks import StockData
from Crawlers.wrapper import wrapper
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import account_activation_token
from .models import DataCollectionUrls
import asyncio


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.core.mail import EmailMessage

import json

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return JsonResponse({"message": "Thank you for your email confirmation. Now you can login your account."})
    else:
        JsonResponse({"message": "Activation link is invalid!"})

def activate_user(request, user, email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        JsonResponse({"message": "Email sent successfully to {email} user, please check your email to activate your account"})
    else:
        JsonResponse({"message": "Something went wrong, please try again later"})


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(json.loads(request.body))
        
        if form.is_valid():

            data = json.loads(request.body)
            
            personalkey = data['personal']
            validate_key = Personalai(personalkey).validate_key()

            if validate_key == False:
                return JsonResponse({"error_message": "Invalid key"})
            
            instance = form.save(commit=False)
            instance.is_staff = data["is_staff"]
            instance.is_active=False
            instance.save()

            Profiles.objects.create(name=instance.username, 
                                    email=data['email'], 
                                    PersonalaiKey=personalkey, 
                                    user= instance.id
                                    )

            activate_user(request, instance, data['email'])

        else:
            return JsonResponse({"error_message": "Invalid form data", "message": form.errors})
    return JsonResponse({"form": "email sent. Please check your email to activate your account"})

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()



@csrf_exempt
def login_user(request):  
    if request.method == 'POST':

        form = LoginForm(json.loads(request.body))

        if form.is_valid():
            payload = json.loads(request.body)
            
            password = payload['password']
            username = payload['username']

            authenticated_user = authenticate(request, 
                                            username=username,
                                            password=password
                                            )

            if authenticated_user is not None:
                login(request, authenticated_user)

                refresh = RefreshToken.for_user(authenticated_user)
                jwt_token = str(refresh.access_token)

                access_token = str(refresh.access_token)

                return JsonResponse({"message": "Logged in successfully",
                                    "access_token": access_token, 
                                    "refresh_token": jwt_token})
            else:
                return JsonResponse({"error_message": "Invalid username or password"})
        
@csrf_exempt
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "You are logged out"})

@csrf_exempt
@permission_classes([IsAuthenticated])
def home(request):
    try:
        keyword = json.loads(request.body)['keyword']
        Wrapper = wrapper(keyword, request.user)
        redirect_page = Wrapper.make_payment()
        return JsonResponse({"redirect_url": redirect_page})
    except Exception as e:
        return JsonResponse({"message": "Something went wrong", "error": str(e)})

@api_view(['GET'])
def payment_success(request):
    if request.GET.get("mode") == "query":
        payment_successful_query(request)
        return JsonResponse({"message": "Payment successful"})
    elif request.GET.get("mode") == "weather":
        payment_successful_weather(request)
        return JsonResponse({"message": "Payment successful"})

def payment_failed(request):
    return JsonResponse({"message": "Payment failed and url upload to personalai failed"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = Profiles.objects.values('id', 'name', 'email', 'updated_time')
    
    json = []
    for user in users:
        user_package = Packages.objects.filter(user=Profiles.objects.get(email=user['email']).user)
        user['usage'] = len(user_package)
        user['queries'] = len(DataCollectionUrls.objects.filter(user=Profiles.objects.get(email=user['email']).user))
        user['total_amount_paid'] = sum([package.price for package in user_package])
        user['total_usage'] = sum([len(package.urls.split(',')) for package in user_package])

        json.append(user)
    
    return JsonResponse({"users": json})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_packages(request):
    packages = Packages.objects.values('id', 'query', 'user', 'price', 'is_active')
    json = []

    user = get_user_model()

    for package in packages:
        package['usage'] = Packages.objects.filter(user=package['user']).count()
        try:
            package['user'] = user.objects.get(id=package['user']).username
        except:
            package['user'] = "None"
        json.append(package)
        
    return JsonResponse({"packages": json})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather(request):
    try:
        city = json.loads(request.body)['city']
        personalkey = Profiles.objects.get(user=request.user.id).PersonalaiKey
        weather_data = WeatherData(personalkey).get_weather_data_by_city_name(city)
        return JsonResponse({"redirect_url": weather_data})
    except Exception as e:
        return JsonResponse({"message": "Something went wrong", "error": str(e)})

def health(request):
    return JsonResponse({"message": "Server is up and running"})

@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        email = json.loads(request.body)['email']
        user = Profiles.objects.get(email=email)
        user.delete()
        User = get_user_model()
        user = User.objects.get(email=email)
        user.delete()
        package = Packages.objects.filter(user=user)
        package.delete()
        DataCollectionUrls.objects.filter(user=user).delete()
        return JsonResponse({"message": "User deleted successfully"})
    except Exception as e:
        return JsonResponse({"message": "User not found"})

@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_package(request):
    package_id = json.loads(request.body)['package_id']
    package = Packages.objects.get(id=package_id)
    package.delete()
    return JsonResponse({"message": "Package deleted successfully"})



def payment_successful_query(request):
    try:
        user_id = Profiles.objects.get(email=request.GET.get("email")).user
        user_package = Packages.objects.filter(user=user_id).last()
    
        user_package.is_active = True
        user_package.save()

        key = Profiles.objects.get(user=user_id).PersonalaiKey
        personalai = Personalai(key)

        string_data = user_package.urls
        urls = string_data[1:-1].split(',')

        urls = [url.strip().strip("'") for url in urls if url.strip().strip("'")]

        response = personalai.upload(urls)
        
        return JsonResponse({"message": "Payment successful" , "response": response})
    except Exception as e:
        return JsonResponse({"message": "Payment successful but urls not uploaded to personalai", "error": str(e)})

def payment_successful_weather(request):
    try:
        profile = Profiles.objects.get(email=request.GET.get("email"))
        
        weatherData = Weather.objects.get(user=profile.user).weatherjson
        
        response = Personalai(profile.PersonalaiKey).memory(str(weatherData))
        
        return JsonResponse({"message": "Payment successful" , "response": response})
    
    except Exception as e:
        return JsonResponse({"message": "Payment successful but urls not uploaded to personalai", "error": str(e)})

@csrf_exempt
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == "GET":
        try:
            return JsonResponse({"packages_count": len(json.loads(serialize('json', Packages.objects.all()))), 
                                "user_count": len(json.loads(serialize('json', Profiles.objects.all()))), 
                                "query_count": len(json.loads(serialize('json', DataCollectionUrls.objects.all()))), 
                                "recent_users": json.loads(serialize('json', Profiles.objects.all().order_by('-updated_time')))
                                })
        except Exception as e:
            return JsonResponse({"message": "Something went wrong", "error": str(e)})
@csrf_exempt
def message(request):
    if request.method == "POST":
        try:
            rbody=json.loads(request.body)
            user_id = rbody['user_id']
            key = Profiles.objects.get(user=user_id).PersonalaiKey
            personalai = Personalai(key)
            message = rbody['message']
            headers={"Content-Type": "application/json",
            "x-api-key": key}
            message_url = 'https://api.personal.ai/v1/message'
            response = requests.post(message_url, headers=headers, json={"Text": message})
            if response.status_code == 200:
                ai_response = response.json()['ai_message']
                print(ai_response)
            return JsonResponse({"message": "Message upload successfully"})
        except Exception as e:
            print(request)
            return JsonResponse({"message": "Something went wrong", "error": str(e)})

@csrf_exempt
@permission_classes([IsAuthenticated])
def cards(request):
    if request.method == "GET":
        try:
            mode = json.loads(request.body)['mode']

            if mode == 'weekly':
                today = datetime.now(timezone.utc)
                dates = [today - timedelta(days=i) for i in range(7)]
                dates = [date.replace(tzinfo=timezone.utc) for date in dates]

                day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                
                data = []

                for date in dates:
                    start_date = date.replace(hour=0, minute=0, second=0)
                    end_date = date.replace(hour=23, minute=59, second=59)
                    profiles = Profiles.objects.filter(updated_time__range=[start_date, end_date])
                    queries = DataCollectionUrls.objects.filter(updated_time__range=[start_date, end_date])
                    income = Packages.objects.filter(updated_time__range=[start_date, end_date]).values('price')
                    income = sum([i['price'] for i in income])
                    urls = [url for query in queries for url in query.urls.split(',')]
                    

                    user_count = len(profiles)

                    day_name = day_names[date.weekday()]
                    data.append({
                        day_name: {
                            "users": user_count,
                            "queries": len(queries),
                            "income": income,
                            "links": len(urls)
                        }
                    })

                return JsonResponse({"cards": data})

            if mode == 'monthly':

                today = datetime.now(timezone.utc)
                dates = [today - timedelta(days=i) for i in range(30)]
                dates = [date.replace(tzinfo=timezone.utc) for date in dates]

                data = []

                for date in dates:
                    start_date = date.replace(hour=0, minute=0, second=0)
                    end_date = date.replace(hour=23, minute=59, second=59)
                    profiles = Profiles.objects.filter(updated_time__range=[start_date, end_date])
                    queries = DataCollectionUrls.objects.filter(updated_time__range=[start_date, end_date])
                    income = Packages.objects.filter(updated_time__range=[start_date, end_date]).values('price')
                    income = sum([i['price'] for i in income])
                    urls = [url for query in queries for url in query.urls.split(',')]
                    

                    user_count = len(profiles)

                    data.append({
                        str(date.date()): {
                            "users": user_count,
                            "queries": len(queries),
                            "income": income,
                            "links": len(urls)
                        }
                    })

                return JsonResponse({"cards": data})
                
            
            if mode == 'yearly':
                today = datetime.now(timezone.utc)
                dates = [today - timedelta(days=i) for i in range(365, 0, -31)]
                dates = [date.replace(tzinfo=timezone.utc) for date in dates]

                data = []

                month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                                'October', 'November', 'December']
                
                

                for date in dates:
                    start_date = date.replace(day =1, hour=0, minute=0, second=0)

                    end_day = 31 if date.month in [1, 3, 5, 7, 8, 10, 12] else 30
                    if date.month == 2:
                        end_day = 28

                    end_date = date.replace(day = end_day,hour=23, minute=59, second=59)
                    profiles = Profiles.objects.filter(updated_time__range=[start_date, end_date])
                    queries = DataCollectionUrls.objects.filter(updated_time__range=[start_date, end_date])
                    income = Packages.objects.filter(updated_time__range=[start_date, end_date]).values('price')
                    income = sum([i['price'] for i in income])
                    urls = [url for query in queries for url in query.urls.split(',')]
                    

                    user_count = len(profiles)

                    month_name = month_names[date.month - 1]

                    data.append({
                        month_name: {
                            "users": user_count,
                            "queries": len(queries),
                            "income": income,
                            "links": len(urls),
                            "date": str(date.date())
                        }
                    })

            return JsonResponse({"cards": data})           

            
        except Exception as e:
            return JsonResponse({"message": "Something went wrong", "error": str(e)})
    return JsonResponse({"cards": []})

@csrf_exempt
@permission_classes([IsAuthenticated])
def get_user_data(request):
    if request.method == "POST":
        try:
            user_id = json.loads(request.body)['user_id']
            user = json.loads(serialize('json', Profiles.objects.filter(user=user_id)))
            total_packages = len(json.loads(serialize('json', Packages.objects.filter(user=user_id))))
            total_amount_paid = sum([package['fields']['price'] for package in json.loads(serialize('json', Packages.objects.filter(user=user_id)))])
            total_links = sum([(len(data_url['fields']['urls'].split(' '))) for data_url in json.loads(serialize('json', DataCollectionUrls.objects.filter(user=user_id)))])
            total_queries = len(json.loads(serialize('json', DataCollectionUrls.objects.filter(user=user_id))))
            return JsonResponse({"user": user, 
                                 "record":
                                 { "total_packages": total_packages,
                                   "total_amount_paid": total_amount_paid,
                                     "total_links": total_links, 
                                     "total_queries": total_queries
                                     }})
        except Exception as e:
            return JsonResponse({"message": "Something went wrong", "error": str(e)})
    else:
        return JsonResponse({"message": "Request must be POST"})

@csrf_exempt
@permission_classes([IsAuthenticated])
def change_user_information(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data['username'] != request.user.username:
            JsonResponse({"message": "You are not allowed to change password of other users"})
        
        try:
            user = User.objects.get(username=data['username'])
            user.set_password(data['password'])
            user.save()
            return JsonResponse({"message": "User password updated successfully"})
        except Exception as e:
            return JsonResponse({"message": "Something went wrong", "error": str(e)})
    return JsonResponse({"message": "Something went wrong"})

@csrf_exempt
@permission_classes([IsAuthenticated])
def get_queries_by_user_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data['user_id'] != request.user.id:
            JsonResponse({"message": "You are not allowed to get queries of other users"})
        try:
            user_id = json.loads(request.body)['user_id']
            queries = json.loads(serialize('json', DataCollectionUrls.objects.filter(user=user_id)))
            return JsonResponse({"queries": queries})
        except Exception as e:
            return JsonResponse({"message": "Something went wrong", "error": str(e)})
    else:
        return JsonResponse({"message": "Request must be POST"})