import os
import json
import requests
import time
from bs4 import BeautifulSoup
from util import current_dir, headers, build_page_url, file_to_array, filepath, send_product_data
from random import randint
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


# User agents
software_names = [SoftwareName.CHROME.value]
operating_systems = [
    OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100)

headers['User-Agent'] = user_agent_rotator.get_random_user_agent()


PAGE_DEPTH = 2

with open(filepath('tokens.json'), 'r') as f:
    tokens = json.load(f)

invalids = file_to_array(filepath('invalid_tags.txt'))


def crawl():
    print('User Agent: ')
    print(headers['User-Agent'])
    print()

    keywords = file_to_array(filepath('search_keywords.txt'))

    page_count = 0
    product_count = 0
    total_product_count = 0

    START_TIME = time.time()

    for keyword in keywords:
        for i in range(1, PAGE_DEPTH + 1):
            url = build_page_url(keyword.strip(), i)
            print('Crawling: ' + url)
            success_pc, total_pc = search_request(url, keyword)
            print()

            if success_pc == 0 and total_pc == 0:
                rl_sleep = 60
                print('Rate limited? wait for ' + str(rl_sleep) + ' seconds')
                time.sleep(rl_sleep)  # Sleep for 1 min

                # Generate new random user agent
                headers['User-Agent'] = user_agent_rotator.get_random_user_agent()
                print('New user agent: ')
                print(headers['User-Agent'])

            product_count += success_pc
            total_product_count += total_pc
            page_count += 1
        print()

    END_TIME = time.time()

    print("Crawled " + str(page_count) + " pages.")
    print("Total products recorded: " +
          str(product_count) + "/" + str(total_product_count))

    print("Took " + str(round(END_TIME - START_TIME) / 60) + " minutes")


def search_request(url: str, category: str):
    try:
        page = requests.get(url, headers=headers, allow_redirects=True)
    except:
        print("Could not send a request to the URL")
        return 0, 0
    parsedPage = BeautifulSoup(page.text, 'html.parser')
    items = parsedPage.find_all(class_='s-result-item')

    success = 0
    count = 0

    for item in items:
        if handle_fields(item, category):
            success += 1
        count += 1

    print("Status: " + str(success) + "/" + str(count))

    wait_time = randint(400, 800)/100
    print("Wait: " + str(wait_time) + " seconds")
    time.sleep(wait_time)

    return success, count


def handle_fields(html: str, category: str) -> bool:
    try:
        title = html.find('h2').text

        for invalid_keyword in invalids:
            t = title.lower()
            if invalid_keyword in t or invalid_keyword + 's' in t:
                return False

        image = html.find('img').get('src')

        link = ''
        product_key = ''
        total_reviews = ''
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
            elif '#customerReviews' in a_link:
                total_reviews = a.find('span').text
                break

        ratings_raw = html.find('i').text
        rating = ratings_raw.split(' ')[0]
        price = html.text.split('$')[1]

        if image == '' or product_key == '' or title == '' or rating == '' or price == '':
            return False

        title = title.strip()
        image = image.strip()
        product_key = product_key.strip()
        link = 'https://www.amazon.com' + link

        brand_name_elem = html.find('h5')
        if brand_name_elem:
            brand = brand_name_elem.find('span').text
            title = brand + ' ' + title

        print_details(title, image, link, product_key, total_reviews,rating, price)

        res = send_product_data(tokens['access_token'], title, '',
                          image, link, product_key, total_reviews, rating, price, category)
        print(res, "\n")

        return True
    except:
        return False


def print_details(title, image, link, product_key, total_reviews, rating, price):
    print("Title: " + title)
    print("Image: " + image)
    print("Product Key: " + product_key)
    print("Link: " + link)
    print("Total reviews: " + total_reviews)
    print("Rating: " + rating)
    print("Price: $" + price)
    print()


if __name__ == "__main__":
    crawl()
