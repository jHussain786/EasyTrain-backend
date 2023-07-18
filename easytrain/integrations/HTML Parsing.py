import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website_info(url):
    """
    Scrapes information from a website.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        tuple: A tuple containing scraped data and information.
            - df (pandas.DataFrame): DataFrame containing scraped data.
            - word_count (int): Word count for the body of the webpage.
            - char_count (int): Character count for the body of the webpage.
    """
    # Send an HTTP GET request to the URL
    response = requests.get(url)

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

    return df, word_count, char_count

# Define the URL of the webpage to scrape
url = 'https://docs.personal.ai/'

# Scrape website information
info_df, word_count, char_count = scrape_website_info(url)

# Print the scraped information
print(info_df)
print("Word count for the body:", word_count)
print("Character count for the body:", char_count)

# ------------------------------
# Logic Steps:
# 1. Send an HTTP GET request to the provided URL.
# 2. Extract the HTML content from the response.
# 3. Parse the HTML content using Beautiful Soup.
# 4. Find the title tag and retrieve its text.
# 5. Find the meta description tag and retrieve its content attribute value.
# 6. Find the meta keywords tag and retrieve its content attribute value.
# 7. Find the meta author tag and retrieve its content attribute value.
# 8. Abbreviate the description to 250 words.
# 9. Calculate the word count by splitting the description string.
# 10. Calculate the character count of the description.
# 11. Create a pandas DataFrame to store the scraped data.
# 12. Return the DataFrame, word count, and character count.
# ------------------------------
