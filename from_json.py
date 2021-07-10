import json
from util import build_page_url, filepath, send_product_data

with open(filepath('products.json'), 'r') as f:
    products = json.load(f)

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxLCJuYW1lIjoiQXlhYW4gU2lkZGlxdWkiLCJlbWFpbCI6Im1vYWhhbW1lZGF5YWFuLmRldkBnbWFpbC5jb20iLCJpbWFnZVVybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdoSUw5N1hsYWJTaXR3V256N012Z3ZBWVZPNkNTSVl4VnJpRmZEMEJnPXM5Ni1jIiwicGhvbmUiOm51bGx9LCJnVG9rZW4iOiJ5YTI5LmEwQVJyZGFNLTlRLW9CQWJBUTVMRlBHTVVfVUttY3dqbVJ6NGgzTWM5OERmQzF6Zm1jRFhmSTA2ZDFKUUw2V29VbUJpbDktT3B5VHAwcGRMNHpwa1RuRkl2WkdqM2ZadV9ub1JWanhicHhGQ1VIazI4UUx1M3I0bHFicjJQMzBFUzhWdEhBMkVoQ01pYUF3NFdCU2Q4U3BlNjRleDBSIiwiaWF0IjoxNjI1OTQzNjUwLCJleHAiOjE2MzExMjc2NTB9.1UgnKgXROqtYQpT6Mza0vqAa8LlUO-TsSO7ZI6XkVUE"

for product in products:
    title = product['title']
    description = product['description']
    imageUrl = product['imageUrl']
    rating = product['rating']
    price = product['price']
    link = product['website']
    product_key = product['productKey']
    category = product['category']['name']

    send_product_data(access_token, title, description, imageUrl,
                      link, product_key, rating, price, category)
