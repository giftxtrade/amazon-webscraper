import os
import json
import requests
import time
from bs4 import BeautifulSoup
from util import current_dir, headers, build_page_url, file_to_array, filepath
from random import randint

tokens_file = os.path.join(current_dir, "tokens.json")
with open(filepath('tokens.json'), 'r') as f:
    tokens = json.load(f)

invalids = file_to_array(filepath('invalid_tags.txt'))

def crawl():
    keywords = file_to_array(filepath('search_keywords.txt'))

    # for keyword in keywords:
    for keyword in ['Amazon Cloud Cam Devices']:
        url = build_page_url(keyword.strip())
        print('Crawling: ' + url)
        search_request(url)
        print()


def search_request(url: str):
    page = requests.get(url, headers=headers, allow_redirects=True)
    parsedPage = BeautifulSoup(page.text, 'html.parser')
    items = parsedPage.find_all(class_='s-result-item')

    success = 0
    count = 0

    for item in items:
        if handle_fields(item):
            success += 1
        count += 1
    
    print("Status: " + str(success) + "/" + str(count))

    wait_time = randint(1, 30)/100
    print("Wait: " + str(wait_time) + " seconds")
    time.sleep(wait_time)


def handle_fields(html: str):
    try:
        title = html.find('h2').text

        for invalid_keyword in invalids:
            if invalid_keyword in title:
                return False

        image = html.find('img').get('src')

        link = ''
        product_key = ''
        for a in html.find_all('a'):
            a_link = a.get('href')
            if '%2Fdp%2F' in a_link:
                link = a_link
                product_key = link.split('%2Fdp%2F')[1].split('%2F')[0]
                break
            elif '/dp/' in a_link:
                link = a_link
                product_key = link.split('/dp/')[1].split('/')[0]
                break

        ratings_raw = html.find('i').text
        rating = ratings_raw.split(' ')[0]
        price = html.text.split('$')[1]

        if image == '' or product_key == '' or title == '' or rating == '' or price == '':
            return False

        # print_details(title, image, link, product_key, rating, price)

        return True
    except:
        return False


def print_details(title, image, link, product_key, rating, price):
    print("Title: " + title)
    print("Image: " + image)
    print("Product Key: " + product_key)
    print("Link: " + link)
    print("Rating: " + rating)
    print("Price: $" + price)
    print()


check_for_invalids()

if __name__ == "__main__":
    crawl()
