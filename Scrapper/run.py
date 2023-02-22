from Scrapper.config import BaseUrl, CNNConfig, Config, KompasConfig
from Scrapper.dataset import is_url_temp_exists, read_temp_progress, read_url_temp, remove_temp_progress, remove_url_temp, save_news, save_temp_progress, save_url_temp
from Scrapper.obj import News
from Scrapper.scrap_cnn import get_multi_pages_cnn, get_news_content_cnn
from Scrapper.scrap_kompas import get_multi_pages_kompas, get_news_content_kompas

from tqdm import tqdm
from typing import List

import time


def get_multi_news_content(config: Config, urls: List[str]) -> List[News]:
    bar = tqdm(desc='Processing News Contents', total=len(urls))
    if config.LAST_ID != 0:
        urls = urls[config.LAST_ID+1:]
        time.sleep(1)
        bar.update(config.LAST_ID)
        
    for url in urls:
        trial = 0
        while True:
            try:
                if config.BASE_URL == BaseUrl.CNN:
                    news = get_news_content_cnn(url)
                elif config.BASE_URL == BaseUrl.Kompas:
                    news = get_news_content_kompas(url)
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

    


def run(config: Config, num_of_page: int):
    temp_progress = read_temp_progress()
    config.update_by_progress(temp_progress)
    is_read_url = is_url_temp_exists()
    
    if is_read_url:
        urls = read_url_temp()
    else:
        if config.BASE_URL == BaseUrl.CNN:
            urls = get_multi_pages_cnn(config.BASE_URL, num_of_page)
        elif config.BASE_URL == BaseUrl.Kompas:
            urls = get_multi_pages_kompas(config.BASE_URL, num_of_page)
        save_url_temp(urls)

    get_multi_news_content(config, urls)
    remove_url_temp()
    remove_temp_progress()


def run_cnn(num_of_page: int):
    print('Starting CNN News Scrapper')
    config = CNNConfig()
    run(config, num_of_page)


def run_kompas(num_of_page: int):
    print('Starting Kompas News Scrapper')
    config = KompasConfig()
    run(config, num_of_page)