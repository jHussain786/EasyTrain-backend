import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import jsonlines

class WebsiteScraper:
    def __init__(self, url):
        self.url = url
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Create a file handler and set the log level to DEBUG
        file_handler = logging.FileHandler('scraper_logs.jsonl')
        file_handler.setLevel(logging.DEBUG)

        # Create a log formatter
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')

        # Set the formatter for the file handler
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        return logger

    def scrape_website_info(self):
        """
        Scrapes information from a website.

        Returns:
            tuple: A tuple containing scraped data and information.
                - df (pandas.DataFrame): DataFrame containing scraped data.
                - word_count (int): Word count for the body of the webpage.
                - char_count (int): Character count for the body of the webpage.
        """
        try:
            self.logger.debug('Scraping website: {}'.format(self.url))
            
            # Send an HTTP GET request to the URL
            response = requests.get(self.url)
            response.raise_for_status()

            # Extract the HTML content from the response
            html_content = response.text

            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the title tag and get its text
            title = soup.title.string if soup.title else ''

            # Find the meta description tag and get its content attribute value
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'] if description_tag else ''

            # Find the meta keywords tag and get its content attribute value
            keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            keywords = keywords_tag['content'] if keywords_tag else ''

            # Find the meta author tag and get its content attribute value
            author_tag = soup.find('meta', attrs={'name': 'author'})
            author = author_tag['content'] if author_tag else ''

            # Abbreviate the content to 250 words
            abbreviated_description = ' '.join(description.split()[:250])

            # Calculate total word and character count for the body
            word_count = len(description.split())
            char_count = len(description)

            # Create a table using pandas DataFrame
            data = {'tag_name': ['<title>', '<meta name="description">', '<meta name="keywords">', '<meta name="author">'],
                    'description': [title, abbreviated_description, keywords, author]}
            df = pd.DataFrame(data)

            self.logger.debug('Website scraped successfully')
            
            return df, word_count, char_count

        except requests.exceptions.RequestException as e:
            self.logger.error('An error occurred while scraping the website: {}'.format(str(e)))
            raise
        except Exception as e:
            self.logger.error('An unexpected error occurred: {}'.format(str(e)))
            raise


# Define the URL of the webpage to scrape
url = 'https://docs.personal.ai/'

# Create an instance of WebsiteScraper and scrape website information
scraper = WebsiteScraper(url)
info_df, word_count, char_count = scraper.scrape_website_info()

# Print the scraped information
print(info_df)
print("Word count for the body:", word_count)
print("Character count for the body:", char_count)
