import csv
import os
from typing import List

from Scrapper.config import TEMP_PROGRESS, TEMP_URL_CSV, Config, DELIMITER_CSV
from Scrapper.obj import News, Progress


def is_url_temp_exists() -> bool:
    return os.path.isfile(TEMP_URL_CSV)

def read_url_temp() -> List[str]:
    print('Read saved urls temp')
    with open(TEMP_URL_CSV, 'r') as f:
        reader = csv.reader(f)
        urls = [url[0] for url in list(reader)]
        print(f'{len(urls)} loaded')
        return urls

def save_url_temp(urls: List[str]) -> None:
    with open(TEMP_URL_CSV, 'w') as f:
        writer = csv.writer(f)
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


def read_temp_progress() -> Progress:
    if os.path.isfile(TEMP_PROGRESS):
        with open (TEMP_PROGRESS, 'r') as f:
            reader = csv.reader(f, delimiter=DELIMITER_CSV)
            data = list(reader)[0]
            progress = Progress()
            progress.Filename = data[0]
            progress.LastId = int(data[1])
            return progress

    return None


def save_temp_progress(config:Config) -> None:
    with open (TEMP_PROGRESS, 'w') as f:
        writer = csv.writer(f, delimiter=DELIMITER_CSV)
        writer.writerow([config.FILENAME, config.LAST_ID])

def remove_temp_progress():
    os.remove(TEMP_PROGRESS)