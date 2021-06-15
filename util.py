import os
from urllib import parse
import requests

current_dir = os.path.dirname(os.path.realpath(__file__))

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


def filepath(filename: str) -> str:
    return os.path.join(current_dir, filename)


def build_page_url(keyword: str, page_number: int = 1) -> str:
    return 'https://www.amazon.com/s?k={keyword}&page={page}'.format(
        keyword=urlize_string(keyword),
        page=page_number
    )


def urlize_string(str: str) -> str:
    return parse.quote(str)


def file_to_array(filepath: str) -> [str]:
    res = []
    file_set = set()
    with open(filepath, 'r') as f:
        for line in f:
            l = line.strip()
            if l == '' or l.startswith("#"):
                continue

            if l in file_set:
                continue
            file_set.add(l)
            res.append(l)

    return res


def send_product_data(access_token, title, description, imageUrl, link, product_key, rating, price, category):
    response = requests.post('http://localhost:3001/products', headers={
        "Contetn-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }, data={
        "title": title,
        "description": description,
        "productKey": product_key,
        "imageUrl": imageUrl,
        "rating": float(rating),
        "price": float(price),
        "currency": "USD",
        "category": category,
        "website": link
    })
    return response
