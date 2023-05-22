import requests

class StockData:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def get_stock_data_by_symbol(self, symbol):
        endpoint = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}'.format(symbol, self.api_key)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()['Global Quote']
            return data
        else:
            return None