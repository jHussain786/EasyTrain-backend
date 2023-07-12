
from django.urls import path
from easytrainapp import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/register/", views.register_user, name="register"),
    path('api/login/', views.login_user, name='login'),
    path('api/query/', views.home, name='home'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/users/', views.get_all_users, name='users'),
    path('api/packages/', views.get_all_packages, name='packages'),
    path('api/payment_success/', views.payment_success, name='payment_success'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', views.dashboard, name='dashboard'),
    path('api/cards/', views.cards, name='card'),
    path('api/get_user_data/', views.get_user_data, name='get_user_data'),
    path('api/change_user_information/', views.change_user_information, name='change_user_information'),


    path('api/payment_failed/', views.payment_failed, name='payment_failed'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('api/weather/', views.weather, name='weather'),

    path('api/delete_user/', views.delete_user, name='delete_user'),
    path('api/delete_package/', views.delete_package, name='delete_package'),
    path('', views.health, name='health')

]
