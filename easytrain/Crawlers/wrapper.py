from . import google_crawler, multi_search_crawler
from easytrainapp.models import DataCollectionUrls

def get_urls(query):
    
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

        datacollection = DataCollectionUrls(word=query, urls=str_urls, updated_time=DataCollectionUrls.get_local_time())
        datacollection.save()
        return urls