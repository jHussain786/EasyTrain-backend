import requests

class WeatherData:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def get_weather_data_by_city_name(self, city_name):
        endpoint = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city_name, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            return data
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