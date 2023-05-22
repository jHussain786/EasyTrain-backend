from . import google_crawler, multi_search_crawler

def get_urls(query):
    urls = []
    urls.extend(google_crawler.get_urls(query))
    urls.extend(multi_search_crawler.MultiSearchCrawler(query).search_news())
    return urls
