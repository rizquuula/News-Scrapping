import csv
import os
from typing import List

from Scrapper.config import TEMP_URL_CSV, Config, DELIMITER_CSV
from Scrapper.obj import News


def save_url_temp(urls: List[str]):
    with open(TEMP_URL_CSV, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for url in urls: 
            writer.writerow([url])


def remove_url_temp():
    os.remove(TEMP_URL_CSV)


def save_news(config:Config, news: News):
    filepath = os.path.join(config.OUTPUT_DIR, config.FILENAME)
    
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as header_only:
            writer = csv.writer(header_only, delimiter=DELIMITER_CSV)
            writer.writerow(news.header())

    with open(filepath, 'a') as f:
        writer = csv.writer(f, delimiter=DELIMITER_CSV)
        writer.writerow(news.to_list())