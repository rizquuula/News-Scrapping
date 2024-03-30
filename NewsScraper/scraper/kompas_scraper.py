import time
from typing import List

from tqdm import tqdm
from NewsScraper.models.news import NewsContent
from NewsScraper.config.scraper_config import ScraperConfig
from NewsScraper.scraper.main_scraper import MainScraper
from NewsScraper.scraper_data.scraper_data import ScraperData
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress
from NewsScraper.scraper_url.scraper_url import ScraperUrl
from NewsScraper.bs4_engine.open_connection import open_bs4_connection


class KompasScraper(MainScraper):
    def __init__(self, 
                 config: ScraperConfig, 
                 progress: ScraperProgress, 
                 news_url: ScraperUrl,
                 dataset: ScraperData):
        super().__init__(config, progress, news_url, dataset)

    def read_urls(self) -> List[str]:
        all_links = []
        for i in tqdm(range(self.config.num_of_page), desc='[ACTIVITY] Processing News Pages:'):
            trial = 0
            while True:
                try:
                    id = 1+i
                    url = f'{self.config.base_url}?page={id}'
                    page_links = self.read_urls_in_news_list(url)
                    all_links.extend(page_links)
                    break
                except Exception as e:
                    trial += 1
                    print('[ERR] Something wrong!!', e)
                    if trial > 5:
                        is_cancel = input('Skip? (y/n) ')
                        if is_cancel.lower() == 'y':
                            break
                        
                    print('[ERR] Retrying in 5 seconds...')
                    time.sleep(5)

        self.news_url.save_url_temp(all_links)
        return all_links
    
    def read_urls_in_news_list(self, page_url: str) -> List[str]:
        soup = open_bs4_connection(page_url)
        
        news_container = soup.find("div", {"class": "latest ga--latest mt2 clearfix -newlayout"})
        news_boxes = news_container.find_all("div", {"class": "article__list"})

        links = []
        for news in news_boxes:
            link_a = news.find('a', {"class": "article__link"}, href=True)
            link = link_a['href']
            links.append(link)
        
        return links

    def scrap_news_content(self, url: str) -> NewsContent:
        soup = open_bs4_connection(url)
        
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

        news = NewsContent(
            title=news_title,
            timestamp=news_timestamp,
            full_text=news_full_text,
            tags=news_tags,
            url=url,
            author=news_author,
        )
        return news
