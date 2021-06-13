import os
from urllib import parse

current_dir = os.path.dirname(os.path.realpath(__file__))

headers = {
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
    with open(filepath, 'r') as f:
        for line in f:
            if not line or line == '' or line.startswith("#"):
                continue
            res.append(line)
    return res
