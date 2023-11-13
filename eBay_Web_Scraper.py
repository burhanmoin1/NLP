import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random

ua = UserAgent()

def get_random_headers():
    return {'User-Agent': ua.random}

def search_ebay(title):
    url = f'https://www.ebay.com/sch/i.html?_nkw={title}'
    
    headers = get_random_headers()
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Parse HTML to extract needed data
    listings = soup.find_all('li', class_='s-item')
    
    prices = []
    for listing in listings:
        price = listing.find('span', class_='s-item__price').text
        prices.append(float(price.replace('$','')))
        
    return sum(prices)/len(prices), url, [listing.a['href'] for listing in listings], len(listings)

def calc_price_diff(export_price, ebay_price):
    return export_price - ebay_price

def main():

    df = pd.read_csv('export.csv')
    
    results = []
    for index, row in df.iterrows():
      
        title = row['title']
      
        avg_price, search_url, item_urls, listings_count = search_ebay(title)
        
        price_diff = calc_price_diff(row['price'], avg_price)
        
        results.append([title, avg_price, search_url, item_urls, price_diff])
        
        # Sleep to avoid overwhelming eBay
        time.sleep(random.randint(2,5))
        
    results_df = pd.DataFrame(results, columns=[
        'title', 'avg_price', 'search_url', 'item_urls', 'price_diff'
    ])
    
    # Sort by price diff
    results_df = results_df.sort_values('price_diff')
    
    # Export CSV
    results_df.to_csv('found.csv', index=False)
    
if __name__ == '__main__':
    main()