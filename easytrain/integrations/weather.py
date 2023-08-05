import requests
from integrations.personalai import Personalai
from easytrainapp.models import Profiles, WeatherData
from .stripe_payment import StripePayment

class Weather:
    def __init__(self):
        self.api_key = "584a2006812ad1d107213c4834e6936c"
        
    def get_weather_payment(userid):
            profile = Profiles.objects.filter(user=userid).first()
            mode = "weather"
            stripe_payment = StripePayment(int(619), profile, mode)
            return stripe_payment.checkout_session() 
        
    def send_weather_data_to_ai(self, city_name,user):
        endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city_name, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            profile = Profiles.objects.filter(user=user).first().PersonalaiKey
            memory_message = "Weather data for " + city_name + "\n"
            for ey, val in data.items():
                memory_message = memory_message + str(ey) + " value: " + str(val)
            status = Personalai(profile).memory(memory_message)
            return status
        else:
            print("The queryset is empty.")
        
    # def get_forecast_payment(self, userid):
    #     profile = Profiles.objects.filter(user=userid).first()
    #     mode = "weather"
    #     stripe_payment = StripePayment(int(1832), profile, mode)
    #     return stripe_payment.checkout_session() 
    
    # def send_forecast_data_TO_ai(self, user,city_name):
    #     params = {
    #     "q": city_name,
    #     "appid": self.api_key
    # }
    #     BASE_URL = "https://api.openweathermap.org/data/2.5/forecast/hourly"
    #     response = requests.get(BASE_URL, params=params)
    #     # endpoint = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'.format(city_name, self.api_key)
    #     # response = requests.get(endpoint)
    #     if response.status_code == 200:
    #         data = response.json()
    #         profile = Profiles.objects.filter(user=user).first().PersonalaiKey
    #         memory_message = "Weather forecast data for " + city_name + "\n"
    #         for ey, val in data.items():
    #             memory_message = memory_message + str(ey) + " value: " + str(val)
    #         status = Personalai(profile).memory(memory_message)
    #         return status
    #     else:
    #          print("Error occurred: Status code", response.status_code)

    # def get_history_payment(self, userid):
    #     profile = Profiles.objects.filter(user=userid).first()
    #     mode = "weather"
    #     stripe_payment = StripePayment(int(1832), profile, mode)
    #     return stripe_payment.checkout_session() 
    
    # def send_history_data_TO_ai(self, user,city_name):
    #     endpoint = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?q={}&appid={}'.format(city_name, self.api_key)
    #     response = requests.get(endpoint)
    #     profile = Profiles.objects.filter(user=user).first().PersonalaiKey
    #     if response.status_code == 200:
    #         data = response.json()
    #         memory_message = "Weather history data for " + city_name + "\n"
    #         for ey, val in data.items():
    #             memory_message = memory_message + str(ey) + " value: " + str(val)
    #         print(data.json)
    #         # status = Personalai(profile).memory(memory_message)
    #         # return status
    #     else:
    #         print("Error occurred: Status code", response.status_code)
    # def send_latlon_data_TO_ai(self, user):
    #         status = Personalai(self.personal_api_key).memory(user)
    #         return status
    # def get_weather_data_by_lat_lon(self, latitude, longitude):
    #     endpoint = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latitude, longitude, self.api_key)
    #     response = requests.get(endpoint)
    #     if response.status_code == 200:
    #         data = response.json()
    #         profile = Profiles.objects.filter(PersonalaiKey=self.personal_api_key).first()
    #         mode = "weather"
    #         stripe_payment = StripePayment(int(self.calculate(data)), profile, mode)
    #         return stripe_payment.checkout_session() 
    #     else:
    #         return None
    
    # def stringly_weather_json(self, weather_json):
    #     weather_string = ''
    #     for weather in weather_json:
    #         weather_string += weather['main'] + ', '
    #     return weather_string
    
    def calculate(self, memory_message):
        total_price = 1
        length = len(memory_message)
        total_price = length + total_price
        return total_price

    
    
    
    
    