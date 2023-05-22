from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from easytrainapp import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path('login/', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', views.login_user, name='login')
]
