import time
from bs4 import BeautifulSoup
from tqdm import tqdm 
from typing import List
from urllib.request import Request, urlopen
from Scrapper.config import Config

from Scrapper.obj import News
from Scrapper.dataset import remove_url_temp, save_news, save_url_temp

def read_page(url:str=None) -> List:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    news_container = soup.find("div", {"class": "list media_rows middle"})
    news_boxes = news_container.find_all("article", {})

    links = []
    for news in news_boxes:
        link_a = news.find('a', href=True)
        link = link_a['href']
        links.append(link)
    
    return links

'latest ga--latest'

def run_kompas(num_of_page: int):
    return 