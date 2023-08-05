
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
    
    # weather api's
    #####
    # call weather to return the Stripe Api for payment
    path('api/weather/', views.weather, name='weather'),
    #after succesfull payment send request to below to send data to personal ai
    path('api/weather/save', views.weather_saving_data_to_ai, name='weathersave'),




    #weather forcast POST using city name it will calculate memory and return the Stripe Api for payment
    # path('api/weatherforcast/', views.weatherforcast, name='weatherforcast'),
    # #after succesfull payment send a GET api to below to send data to personal ai for Forcast
    # path('api/weatherforcast/save', views.weatherforcast_saving_data_to_ai, name='weatherforcast_saving_data_to_ai'),
    # #weather history POST using city name it will calculate memory and return the Stripe Api for payment
    # path('api/weatherhistory/', views.weatherhistory, name='weatherhistory'),
    #  #after succesfull payment send a GET api to below to send data to personal ai for history
    # path('api/weatherhistory/save', views.weatherhistory_saving_data_to_ai, name='weatherhistory_saving_data_to_ai'),
    #  #weather POST using Latitute Longitute it will calculate memory and return the Stripe Api for payment
    # path('api/weatherlatlon/', views.weatherlatlon, name='weatherlatlon'),
    #  #after succesfull payment send a GET api to below to send data to personal ai for data using Latitute Longitute
    # path('api/weatherlatlon/save', views.weatherlatlon_saving_data_to_ai, name='weatherlatlon_saving_data_to_ai'),


#stocks
####
#returns stocks payment from stripe
    path('api/stock/', views.stock, name='stock'),
#saves stocks from the symbol to ai    
    path('api/stock_data_by_symbol/', views.stock_data_by_symbol, name='stock_data_by_symbol'),
#gets all related words to the basically searching stocks
    path('api/stock_search/', views.stock_search, name='stock_search'),

    path('api/delete_user/', views.delete_user, name='delete_user'),
    path('api/delete_package/', views.delete_package, name='delete_package'),
    path('api/get_queries/', views.get_queries_by_user_id, name='get_queries_by_user_id'),
    path('', views.health, name='health'),

]
