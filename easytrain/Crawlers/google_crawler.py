"""
Author: Matthew Schafer
Date: April 17, 2023
Description: A script to search Google for "land mobile radio companies" and show number of results and URLS in a list.
Replace: query with your search query
"""

from googlesearch import search

def get_urls(query):
    search_results = search(query, num_results=10)  
    urls = []
    for idx, result in enumerate(search_results):
        try:
            urls.append(result)
        except Exception as e:
            print(f"Error processing search result {idx + 1}: {e}")
    print(urls)
    return urls
