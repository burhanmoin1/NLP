import requests
from bs4 import BeautifulSoup
import os
import random
import time
url="https://sacramento.craigslist.org/search/sacramento-ca/sss?lat=38.5817&lon=-121.493&query=selling&search_distance=60#search=1~gallery~0~0"

# Remove existing export.csv file if it exists
try:
    os.remove('export.csv')
except FileNotFoundError:
    pass

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
# Initialize the starting page number
s = 0

# Continuously scrape listings until no more results are found
while True:
    # Increment the page number to move to the next page
    s += 120

    # Print a message indicating the current page being scraped
    print(f"Scraping page {s}")

    # Add a random delay to avoid overloading the website
    time.sleep(random.randint(3, 5))

    # Send a GET request to the current page URL
    response = requests.get(f"{url}&s={s}")