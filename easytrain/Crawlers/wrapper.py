from . import google_crawler, multi_search_crawler
from easytrainapp.models import DataCollectionUrls
from datetime import datetime
from django.shortcuts import redirect
from integrations.stripe_payment import StripePayment
from integrations.personalai import Personalai



class wrapper:
    def __init__(self, query, user):
        self.query = query
        self.user = user
        self.urls = []

    def make_payment(self):
        price = int(self.calculate_price())

        personalai = Personalai(self.user.PersonalaiKey)
        ids = personalai.upload(self.urls)

        stripe = StripePayment(price)
        stripe_page = stripe.checkout_session()['url']

        return stripe_page

    def calculate_price(self):
        urls = self.get_urls()
        
        return len(urls) * 0.01 * 100 + 1
        
    def get_urls(self):
        
        if DataCollectionUrls.objects.filter(word= self.query).exists():
            return self.get_urls_from_db()
        else:
            return self.get_urls_from_crawlers()
    

    def get_urls_from_db(self):
        datacollection = DataCollectionUrls.objects.get(word= self.query)
        return datacollection.urls
    
    def get_urls_from_crawlers(self):

        self.urls.extend(google_crawler.get_urls(self.query))
        self.urls.extend(multi_search_crawler.MultiSearchCrawler(self.query).search_news())
        
        str_urls = ""
        for url in self.urls:
            str_urls += url + " "

        datacollection = DataCollectionUrls(word=self.query , urls=str_urls, updated_time= datetime.now())
        datacollection.save()

        return self.urls
    
    