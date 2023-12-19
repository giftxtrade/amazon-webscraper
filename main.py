import locale
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

headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Cookie'] = 'session-id=138-6039432-2778668; session-id-time=2082787201l; i18n-prefs=USD; csm-hit=tb:s-8WA567V0RYP3HZ0WKC9K|1702961621677&t:1702961623277&adb:adblk_no; ubid-main=131-5507218-3142957; session-token=v3EmbwXd6LYH/rgfctopbElCfMOLXelKBluastm10kZVEzoDYV9Kq41Jbm/DXhQNh0PZDCYhxIJoFrj5tHVeLmlUh1yXb8zo5T6elOLeXyRHKItv1BQ+5qoS1s7exjDpWcGVo6zZAGeHMqfGQxeuNdjipxrloT7HvQWhSRF9lHdbMQT2it2RxnACPpxlCto7eiuHQ09T7YCG/X1UuWzcbHpce90hCTXCtsNPL2TeEet1Y3XcTq9Dh8P7oOaZQCthuMYOHvdfuXR8zocEHlTdTvyvXh0uKpXVyCLHUax2jDIJjcGez1gbCDegKQmeAHdMyxNSfwDCRnFyaEYeJySNZ18DeJcLX+B2'
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


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
                headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
                print('New user agent: ')
                print(headers['User-Agent'])

            product_count += success_pc if success_pc >= 0 else 0
            total_product_count += total_pc if total_pc >= 0 else 0
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
        return -1, -1
    parsedPage = BeautifulSoup(page.text, 'html.parser')
    items = parsedPage.find_all(class_='s-result-item')

    if len(items) == 0 and ('Sorry!' in parsedPage.find('title').text):
        print('bot was identified :(')
        return -1, -1

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
        total_reviews = 0
        for a in html.find_all('a'):
            a_link = a.get('href')
            if '%2Fdp%2F' in a_link:
                link = a_link
                product_key = link.split('%2Fdp%2F')[1].split('%2F')[0]
            elif '/dp/' in a_link:
                link = a_link
                product_key = link.split('/dp/')[1].split('/')[0]
            
            if '#customerReviews' in a_link:
                total_reviews = locale.atoi(a.find('span').text)

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
    print("Total reviews: " + str(total_reviews))
    print("Rating: " + rating)
    print("Price: $" + price)
    print()


if __name__ == "__main__":
    crawl()
