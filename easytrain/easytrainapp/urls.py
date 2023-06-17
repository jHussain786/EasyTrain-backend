from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from easytrainapp import views

urlpatterns = [
    path("api/register/", views.register_user, name="register"),
    path('api/login/', views.login_user, name='login'),
    path('api/home/', views.home, name='home'),
    path('api/logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('api/users/', views.get_all_users, name='users'),
    path('api/packages/', views.get_all_packages, name='packages'),
    path('api/payment_success/', views.payment_success, name='payment_success')
]
