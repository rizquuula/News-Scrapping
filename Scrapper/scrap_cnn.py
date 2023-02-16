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


def get_multi_pages(base_url:str, num_of_pages:int) -> List[str]:
    all_links = []
    for i in tqdm(range(num_of_pages), desc='Processing News Pages:'):
        id = 1+i
        url = f'{base_url}{id}'
        page_links = read_page(url)
        all_links.extend(page_links)
    return all_links


def get_news_content(url:str) -> News:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    
    news_title = soup.find("h1", {"class": "title"}).text.strip()
    news_timestamp = soup.find("div", {"class": "date"}).text.strip()
    news_full_text = soup.find("div", {"id": "detikdetailtext"}).text.strip()
    
    news_tag_div = soup.find("div", {"class": "list-topik-terkait"})
    news_tags = news_tag_div.find_all("a")
    news_tags = [tag.text.strip() for tag in news_tags]
    news_tags = ';'.join(news_tags)
    
    news_author = soup.find("div", {"class": "author"}).text.strip()

    news = News()
    news.Title = news_title
    news.Timestamp = news_timestamp
    news.FullText = news_full_text
    news.Tags = news_tags
    news.Url = url
    news.Author = news_author
    
    return news


def get_multi_news_content(config: Config, urls: List[str]) -> List[News]:
    for url in tqdm(urls, desc='Processing News Contents'):
        news = get_news_content(url)
        save_news(config, news)

def run_cnn(config: Config, num_of_page: int):
    urls = get_multi_pages(config.BASE_URL, num_of_page)
    save_url_temp(urls)

    get_multi_news_content(config, urls)
    
    remove_url_temp()