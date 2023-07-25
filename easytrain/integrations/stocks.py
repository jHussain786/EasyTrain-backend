import json
import requests
from easytrainapp.models import Profiles

from integrations.personalai import Personalai
from integrations.stripe_payment import StripePayment

class StockData:
    def __init__(self):
        self.api_key = '75IM217MQN0IW1G0'

    def get_stock_payment(userid):
            profile = Profiles.objects.filter(user=userid).first()
            mode = "stock"
            stripe_payment = StripePayment(int(1735), profile, mode)
            return stripe_payment.checkout_session()   
      
    def get_stock_data_by_symbol(self,symbol,user):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        data_str = json.dumps(data)
        profile = Profiles.objects.filter(user=user).first().PersonalaiKey
        num_tokens = len(data_str.split())
        print("Number of tokens:", num_tokens)
        status = Personalai(profile).memory(data)
        return status
    def keyword_search(self,word):
        print(word)
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={word}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        return data
    
    def calculate(self, memory_message):
        total_price = 1
        length = len(memory_message)
        total_price = length + total_price
        return total_price