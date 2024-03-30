import csv
import os
from typing import List

from NewsScraper.config.scraper_config import ScraperConfig
from NewsScraper.models.news import NewsContent
from NewsScraper.static_vars import *


class ScraperData:
    data: List[NewsContent]
    output_dir: str
    filename: str

    def __init__(
        self, 
        output_dir: str, 
        filename: str
        ) -> None:
        self.data = []
        self.output_dir = output_dir
        self.filename = filename
    
    def delete_data(self):
        if self.is_data_file_exists():
            os.remove(self.__get_filepath())
    
    def load_data(self):
        with open(self.__get_filepath(), 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                news = NewsContent.new_from_array(row)
                self.data.append(news)
        
    def append_data(self, news: NewsContent) -> NewsContent:
        self.data.append(news)
        self.__save_data_to_file(news)
        return self.data[-1]
    
    def is_data_file_exists(self):
        return os.path.isfile(self.__get_filepath())
    
    def __get_filepath(self):
        return os.path.join(self.output_dir, self.filename)
    
    def __create_init_file(self):
        if not self.is_data_file_exists():
            with open(self.__get_filepath(), 'w') as header_only:
                writer = csv.writer(header_only, delimiter=DELIMITER_CSV)
                writer.writerow(NewsContent.header())
                
    def __save_data_to_file(self, news: NewsContent):
        self.__create_init_file()
        
        with open(self.__get_filepath(), 'a') as f:
            writer = csv.writer(f, delimiter=DELIMITER_CSV)
            writer.writerow(news.to_list())
