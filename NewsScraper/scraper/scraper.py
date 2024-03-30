from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from NewsScraper.models.news import NewsContent
from NewsScraper.config.scraper_config import ScraperConfig
from NewsScraper.scraper_data.scraper_data import ScraperData
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress
from NewsScraper.scraper_url.scraper_url import ScraperUrl


@dataclass
class Scraper(ABC):
    config: ScraperConfig
    progress: ScraperProgress
    news_url: ScraperUrl
    dataset: ScraperData
    
    @abstractmethod
    def run_scraper(self) -> ScraperData:
        ...

    @abstractmethod
    def read_urls(self) -> List[str]:
        ...
    
    @abstractmethod
    def read_urls_in_news_list(self, page_url: str) -> List[str]:
        ...
    
    @abstractmethod
    def scrap_news_content(self, url: str) -> NewsContent:
        ...
