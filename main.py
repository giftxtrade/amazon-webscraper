import requests
from bs4 import BeautifulSoup


def main():
    URL = 'https://www.amazon.com/Beauty-Makeup-Skin-Hair-Products/b/?ie=UTF8&node=3760911'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    page = requests.get(URL, headers=headers)
    parsedPage = BeautifulSoup(page.text, 'html.parser')

    # inner = parsedPage.find(
    #     'ul.a-unordered-list a-nostyle a-horizontal octopus-pc-card-list octopus-pc-card-height-v3-with-prime-badge')
    print(parsedPage.prettify())


if __name__ == "__main__":
    main()
