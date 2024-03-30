from typing import List
from tqdm import tqdm
from NewsScraper.models.news import NewsContent
from NewsScraper.config.scraper_config import ScraperConfig
from NewsScraper.scraper_data.scraper_data import ScraperData
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress
from NewsScraper.scraper.scraper import Scraper
from NewsScraper.scraper_url.scraper_url import ScraperUrl

import time


class MainScraper(Scraper):
    def __init__(self, 
                 config: ScraperConfig, 
                 progress: ScraperProgress, 
                 news_url: ScraperUrl,
                 dataset: ScraperData):
        super().__init__(config, progress, news_url, dataset)

    def run_scraper(self) -> ScraperData:
        if self.config.overwrite:
            # if overwrite, delete all temp and data then start from zero
            self.news_url.delete_url_temp()
            self.progress.delete_progress()
            self.dataset.delete_data()
        else:
            if not self.news_url.is_url_temp_exists() \
                and not self.progress.is_temp_progress_exists() \
                and self.dataset.is_data_file_exists():
                raise FileNotFoundError(
                    f'Data file ({self.config.filename}) exists while TEMP file missing for overwrite=False. \
Choose different filename or set overwrite=True.')
            
        # read temp url
        self.news_url.read_url_temp()
        if len(self.news_url.urls) == 0:
            self.read_urls()
        else:
            print('[ACTIVITY] Using URLs from temp file.')
        
        # read temp progress
        self.progress.read_progress()
        if self.progress.last_id != 0:
            print('[ACTIVITY] Using progress from temp file.')
            self.dataset.filename = self.progress.filename
            self.dataset.load_data()
        
        # process scraper
        progress_bar = tqdm(desc='[ACTIVITY] Processing News Contents', total=len(self.news_url.urls))
        time.sleep(0.5) # wait for terminal to response
        progress_bar.update(self.progress.last_id)
        
        for url in self.news_url.urls[self.progress.last_id:]:
            trial = 0
            while True:
                try:
                    news = self.scrap_news_content(url)
                    self.dataset.append_data(news)
                    
                    # update progress
                    self.progress.update_progress(self.progress.last_id+1)
                    progress_bar.update(1)
                    break
                
                except Exception as e:
                    trial += 1
                    print('[ERR] Something wrong (2)!!', e)
                    if trial > 5:
                        is_cancel = input('Skip? (y/n) ')
                        if is_cancel.lower() == 'y':
                            break
                        
                    print('[ERR] Retrying in 5 seconds...')
                    time.sleep(5)
                    
        self.news_url.delete_url_temp()
        self.progress.delete_progress()
        
        return self.dataset
    
    def read_urls(self) -> List[str]:
        raise NotImplementedError()

    def read_urls_in_news_list(self, page_url: str) -> List[str]:
        raise NotImplementedError()

    def scrap_news_content(self, url: str) -> NewsContent:
        raise NotImplementedError()
