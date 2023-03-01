from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from Scrapper.config import TempoConfig
from Scrapper.obj import News
from tqdm import tqdm 
from typing import List
from urllib.request import Request, urlopen

import time


def read_page_tempo(url:str=None) -> List:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    news_container = soup.find("main", {"class": "main-left"})
    news_boxes = news_container.find_all("div", {"class": "card-box ft240 margin-bottom-sm"})

    links = []
    for news in news_boxes:
        link_a = news.find('a', href=True)
        link = link_a['href']
        links.append(link)
    
    return links


def get_multi_pages_tempo(config:TempoConfig) -> List[str]:
    all_links = []
    start_date_obj = datetime.strptime(config.START_DATE, "%Y-%m-%d")

    for single_date in (start_date_obj + timedelta(n) for n in tqdm(range(config.NUM_OF_DAY), desc='Processing News Pages:')):
        single_date_str = single_date.strftime("%Y-%m-%d")
        trial = 0
        while True:
            try:
                url = config.BASE_URL.replace('YYYY-MM-DD', single_date_str)
                page_links = read_page_tempo(url)
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


def get_news_content_tempo(url:str) -> News:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    
    news_title = soup.find("h1", {"class": "title margin-bottom-sm"})
    news_title = news_title.text.strip() if news_title is not None else ''

    news_timestamp = soup.find("p", {"class": "date margin-bottom-sm"})
    news_timestamp = news_timestamp.text.strip() if news_timestamp is not None else ''

    news_full_text = soup.find("div", {"id": "isi"})
    if not news_full_text:
        news_full_text = soup.find("div", {"class": "detail-in"})
        
    news_full_text = news_full_text.text.strip() if news_full_text is not None else ''
    
    news_tag_div = soup.find("div", {"class": "box-tag-detail"})
    if news_tag_div:
        news_tags = news_tag_div.find_all("a")
        news_tags = [tag.text.strip() if tag is not None else '' for tag in news_tags]
        news_tags = ';'.join(news_tags)
    else:
        news_tags = ''
    
    news_author = soup.find("div", {"class": "block-avatar margin-bottom-sm"})
    news_author = news_author.text.strip() if news_author is not None else ''
    news_author = news_author.replace('\n', ' ')
    news_author = re.sub(' +', ' ', news_author)

    news = News()
    news.Title = news_title
    news.Timestamp = news_timestamp
    news.FullText = news_full_text
    news.Tags = news_tags
    news.Url = url
    news.Author = news_author
    
    return news