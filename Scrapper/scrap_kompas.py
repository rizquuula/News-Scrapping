import time
from bs4 import BeautifulSoup
from tqdm import tqdm 
from typing import List
from urllib.request import Request, urlopen
from Scrapper.config import Config, KompasConfig

from Scrapper.obj import News
from Scrapper.dataset import is_url_temp_exists, read_temp_progress, read_url_temp, remove_url_temp, save_news, save_temp_progress, save_url_temp

def read_page(url:str=None) -> List:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    news_container = soup.find("div", {"class": "latest ga--latest mt2 clearfix -newlayout"})
    news_boxes = news_container.find_all("div", {"class": "article__list"})

    links = []
    for news in news_boxes:
        link_a = news.find('a', {"class": "article__link"}, href=True)
        link = link_a['href']
        links.append(link)
    
    return links


def get_multi_pages(base_url:str, num_of_pages:int) -> List[str]:
    all_links = []
    for i in tqdm(range(num_of_pages), desc='Processing News Pages:'):
        trial = 0
        while True:
            try:
                id = 1+i
                url = f'{base_url}?page={id}'
                page_links = read_page(url)
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


def get_news_content(url:str) -> News:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    
    news_title = soup.find("h1", {"class": "read__title"})
    news_title = news_title.text.strip() if news_title is not None else ''

    news_timestamp = soup.find("div", {"class": "read__time"})
    news_timestamp = news_timestamp.text.strip() if news_timestamp is not None else ''

    if not news_timestamp:
        # check on video website
        news_timestamp = soup.find("div", {"class": "videoKG-date"})
        news_timestamp = news_timestamp.text.strip() if news_timestamp is not None else ''


    news_full_text = ''
    news_content = soup.find("div", {"class": "read__content"})
    if news_content:
        paragraph_content = news_content.find_all("p")
        if len(paragraph_content) > 0:
            full_text = []
            for text_content in paragraph_content:
                text = text_content.text.strip()
                if "Baca juga" not in text:
                    full_text.append(text)

            news_full_text = ' '.join(full_text)
    
    news_tags = ''
    news_tag_ul = soup.find("ul", {"class": "tag__article__wrap"})
    if news_tag_ul:
        news_tags = news_tag_ul.find_all("li")
        news_tags = [tag.text.strip() if tag is not None else '' for tag in news_tags]
        news_tags = ';'.join(news_tags)

    if not news_tags:
        # check on video website
        news_tag_content = soup.find("div", {"class": "videoKG-tag"})
        if news_tag_content:
            news_tag_ul = news_tag_content.find("ul")
            if news_tag_ul:
                news_tags = news_tag_ul.find_all("li")
                news_tags = [tag.text.strip() if tag is not None else '' for tag in news_tags]
                news_tags = ';'.join(news_tags)
    
    news_author = soup.find("div", {"class": "read__credit clearfix"})
    news_author = news_author.text.strip() if news_author is not None else ''

    news = News()
    news.Title = news_title
    news.Timestamp = news_timestamp
    news.FullText = news_full_text
    news.Tags = news_tags
    news.Url = url
    news.Author = news_author
    
    return news


def get_multi_news_content(config: Config, urls: List[str]) -> List[News]:
    bar = tqdm(desc='Processing News Contents', total=len(urls))
    if config.LAST_ID is not None:
        urls = urls[config.LAST_ID+1:]
        time.sleep(1)
        bar.update(config.LAST_ID)

    for url in urls:
        trial = 0
        while True:
            try:
                news = get_news_content(url)
                save_news(config, news)
                
                # update progress
                config.LAST_ID+=1
                save_temp_progress(config.FILENAME, config.LAST_ID)
                bar.update(1)
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


def run_kompas(num_of_page: int):
    print('Starting Kompas News Scrapper')
    config = KompasConfig()
    
    temp_progress = read_temp_progress()
    config.update_by_progress(temp_progress)
    is_read_url = is_url_temp_exists()

    if is_read_url():
        urls = read_url_temp()
    else:
        urls = get_multi_pages(config.BASE_URL, num_of_page)
        save_url_temp(urls)

    get_multi_news_content(config, urls)
    remove_url_temp()