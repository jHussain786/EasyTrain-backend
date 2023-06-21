from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from easytrainapp import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/register/", views.register_user, name="register"),
    path('api/login/', views.login_user, name='login'),
    path('api/query/', views.home, name='home'),
    path('api/logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('api/users/', views.get_all_users, name='users'),
    path('api/packages/', views.get_all_packages, name='packages'),
    path('api/payment_success/', views.payment_success, name='payment_success'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/payment_failed/', views.payment_failed, name='payment_failed'),
    path('api/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/weather/', views.weather, name='weather'),
    path('api/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.health, name='health')

]
