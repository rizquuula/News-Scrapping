from datetime import datetime, timedelta
import re
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


class TempoScraper(MainScraper):
    def __init__(self, 
                 config: ScraperConfig, 
                 progress: ScraperProgress, 
                 news_url: ScraperUrl,
                 dataset: ScraperData):
        super().__init__(config, progress, news_url, dataset)

    def read_urls(self) -> List[str]:
        all_links = []
        start_date_obj = datetime.strptime(self.config.start_date, "%Y-%m-%d")

        for single_date in (start_date_obj + timedelta(n) for n in tqdm(range(self.config.num_of_page), desc='Processing News Pages:')):
            single_date_str = single_date.strftime("%Y-%m-%d")
            trial = 0
            while True:
                try:
                    url = self.config.base_url.replace('YYYY-MM-DD', single_date_str)
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
        
        news_container = soup.find("main", {"class": "main-left"})
        news_boxes = news_container.find_all("div", {"class": "card-box ft240 margin-bottom-sm"})

        links = []
        for news in news_boxes:
            link_a = news.find('a', href=True)
            link = link_a['href']
            links.append(link)
        
        return links

    def scrap_news_content(self, url: str) -> NewsContent:
        soup = open_bs4_connection(url)
        
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

        news = NewsContent(
            title=news_title,
            timestamp=news_timestamp,
            full_text=news_full_text,
            tags=news_tags,
            url=url,
            author=news_author,
        )
        return news
