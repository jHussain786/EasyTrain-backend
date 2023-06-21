from . import google_crawler, multi_search_crawler
from easytrainapp.models import DataCollectionUrls
from datetime import datetime
<<<<<<< Updated upstream

def get_urls(query):
=======
from easytrainapp.models import Profiles, Packages
from django.shortcuts import redirect
from integrations.stripe_payment import StripePayment
from integrations.personalai import Personalai



class wrapper:
    def __init__(self, query, user):
        self.query = query
        self.user = user
        self.urls = self.get_urls()

    def make_payment(self):
        price = int(self.calculate_price())
        stripe = StripePayment(price)
        stripe_page = stripe.checkout_session()['url']

        print(self.urls)

        Packages.objects.create(name=self.query, 
                                urls= self.urls,
                                price=price, 
                                is_active=False,
                                user=self.user.id
                                )

        return stripe_page

    def calculate_price(self): 
        characters = 0
        for url in self.urls:
            characters += len(url) 
        return characters * 0.01 * 100 + 1
        
    def get_urls(self):
        
        if DataCollectionUrls.objects.filter(word= self.query).exists():
            return self.get_urls_from_db()
        else:
            return self.get_urls_from_crawlers()
>>>>>>> Stashed changes
    
    if DataCollectionUrls.objects.filter(word=query).exists():
        datacollection = DataCollectionUrls.objects.get(word=query)
        return datacollection.urls.split(" ")
    
    else:
        urls = []
        urls.extend(google_crawler.get_urls(query))
        urls.extend(multi_search_crawler.MultiSearchCrawler(query).search_news())

        str_urls = ""
        for url in urls:
            str_urls += url + " "

        datacollection = DataCollectionUrls(word=query, urls=str_urls, updated_time= datetime.now())
        datacollection.save()
        return urls