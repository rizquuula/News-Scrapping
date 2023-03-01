from bs4 import BeautifulSoup
from Scrapper.config import CNNConfig
from Scrapper.obj import News
from tqdm import tqdm 
from typing import List
from urllib.request import Request, urlopen

import time


def read_page_cnn(url:str=None) -> List:
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


def get_multi_pages_cnn(config:CNNConfig) -> List[str]:
    all_links = []
    for i in tqdm(range(config.NUM_OF_PAGE), desc='Processing News Pages:'):
        trial = 0
        while True:
            try:
                id = 1+i
                url = f'{config.BASE_URL}{id}'
                page_links = read_page_cnn(url)
                all_links.extend(page_links)
                break
            except Exception as e:
                trial += 1
                print('Something wrong!!', e)
                if trial > 5:
                    is_cancel = input('Skip? (y/n) ')
                    if is_cancel.lower() == 'y':
                        break
                    
                print('Retrying in 5 seconds...')
                time.sleep(5)

    return all_links


def get_news_content_cnn(url:str) -> News:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    
    news_title = soup.find("h1", {"class": "title"})
    news_title = news_title.text.strip() if news_title is not None else ''

    news_timestamp = soup.find("div", {"class": "date"})
    news_timestamp = news_timestamp.text.strip() if news_timestamp is not None else ''

    news_full_text = soup.find("div", {"id": "detikdetailtext"})
    if not news_full_text:
        news_full_text = soup.find("div", {"class": "detail_text"})
    news_full_text = news_full_text.text.strip() if news_full_text is not None else ''
    
    news_tag_div = soup.find("div", {"class": "list-topik-terkait"})
    if news_tag_div:
        news_tags = news_tag_div.find_all("a")
        news_tags = [tag.text.strip() if tag is not None else '' for tag in news_tags]
        news_tags = ';'.join(news_tags)
    else:
        news_tags = ''
    
    news_author = soup.find("div", {"class": "author"})
    news_author = news_author.text.strip() if news_author is not None else ''

    news = News()
    news.Title = news_title
    news.Timestamp = news_timestamp
    news.FullText = news_full_text
    news.Tags = news_tags
    news.Url = url
    news.Author = news_author
    
    return news
