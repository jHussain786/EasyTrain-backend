import requests
from integrations.personalai import Personalai
from easytrainapp.models import Profiles, WeatherData
from .stripe_payment import StripePayment

class WeatherData:
    def __init__(self, personal_api_key):
        self.api_key = "584a2006812ad1d107213c4834e6936c"
        self.personal_api_key = personal_api_key
        
    def get_weather_data_by_city_name(self, city_name):
        endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city_name, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()

            memory_message = "Weather data for " + city_name + "\n"
            for ey, val in data.items():
                memory_message = memory_message + str(ey) + " value: " + str(val)

            profile = Profiles.objects.get(PersonalaiKey=self.personal_api_key)
            
            WeatherData.objects.create(city_name=city_name, user=profile.user, weatherjson=data)

            mode = "weather"
            stripe_payment = StripePayment(int(self.calculate(memory_message)), profile, mode)

            return stripe_payment.checkout_session() 
        else:
            return None
        
    def get_forecast_data_by_city_name(self, city_name):
        endpoint = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'.format(city_name, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:

            data = response.json()
            memory_message = "Weather forecast data for " + city_name + "\n"
            for ey, val in data.items():
                memory_message = memory_message + str(ey) + " value: " + str(val)

            status = Personalai(self.personal_api_key).memory(memory_message)
            return status
        else:
            return None
        
    def get_history_data_by_city_name(self, city_name):
        endpoint = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?q={}&appid={}'.format(city_name, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            memory_message = "Weather history data for " + city_name + "\n"
            for ey, val in data.items():
                memory_message = memory_message + str(ey) + " value: " + str(val)


            status = Personalai(self.personal_api_key).memory(memory_message)
            return status
        else:
            return None
    
    def get_weather_data_by_lat_lon(self, latitude, longitude):
        endpoint = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latitude, longitude, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    
    def stringly_weather_json(self, weather_json):
        weather_string = ''
        for weather in weather_json:
            weather_string += weather['main'] + ', '
        return weather_string
    
    def calculate(self, memory_message):
        total_price = 1
        length = len(memory_message)
        total_price = length + total_price

        return total_price

        