import csv
import os
from typing import List, Optional

from NewsScraper.static_vars import *


class ScraperUrl:    
    def __init__(self) -> None:
        self.urls = []
    
    def is_url_temp_exists(self) -> bool:
        return os.path.isfile(TEMP_URL_CSV)

    def read_url_temp(self) -> Optional[List[str]]:
        urls = []
        if self.is_url_temp_exists():
            with open(TEMP_URL_CSV, 'r') as f:
                reader = csv.reader(f)
                for url in reader:
                    urls.append(url[0])
                    
        self.urls = urls
        return self.urls

    def save_url_temp(self, urls: List[str]) -> List[str]:
        with open(TEMP_URL_CSV, 'w') as f:
            writer = csv.writer(f)
            for url in urls: 
                writer.writerow([url])
        self.urls = urls
        return self.urls

    def delete_url_temp(self):
        if self.is_url_temp_exists():
            os.remove(TEMP_URL_CSV)