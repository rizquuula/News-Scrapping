from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def open_bs4_connection(url: str) -> BeautifulSoup:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    return soup
