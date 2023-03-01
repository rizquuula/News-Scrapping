import sys
from Scrapper.config import BaseUrl, CNNConfig, Config, KompasConfig, TempoConfig, TurnbackhoaxConfig
from Scrapper.dataset import is_url_temp_exists, read_temp_progress, read_url_temp, remove_temp_progress, remove_url_temp, save_news, save_temp_progress, save_url_temp
from Scrapper.obj import News
from Scrapper.scrap_cnn import get_multi_pages_cnn, get_news_content_cnn
from Scrapper.scrap_kompas import get_multi_pages_kompas, get_news_content_kompas

from tqdm import tqdm
from typing import List

import time

from Scrapper.scrap_tempo import get_multi_pages_tempo, get_news_content_tempo
from Scrapper.scrap_turnbackhoax import get_multi_pages_turnbackhoax, get_news_content_turnbackhoax


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
                elif config.BASE_URL == BaseUrl.Tempo:
                    news = get_news_content_tempo(url)
                elif config.BASE_URL == BaseUrl.Turnbackhoax:
                    news = get_news_content_turnbackhoax(url)

                save_news(config, news)
                
                # update progress
                config.LAST_ID+=1
                save_temp_progress(config)
                bar.update(1)
                break
            except Exception as e:
                trial += 1
                print('Something wrong (2)!!', e)
                if trial > 5:
                    is_cancel = input('Skip? (y/n) ')
                    if is_cancel.lower() == 'y':
                        break
                    
                print('Retrying in 5 seconds...')
                time.sleep(5)

    


def run(config:Config):
    temp_progress = read_temp_progress()
    config.update_by_progress(temp_progress)
    is_read_url = is_url_temp_exists()
    
    if is_read_url:
        urls = read_url_temp()
    else:
        if config.BASE_URL == BaseUrl.CNN:
            urls = get_multi_pages_cnn(config)
        elif config.BASE_URL == BaseUrl.Kompas:
            urls = get_multi_pages_kompas(config)
        elif config.BASE_URL == BaseUrl.Tempo:
            urls = get_multi_pages_tempo(config)
        elif config.BASE_URL == BaseUrl.Turnbackhoax:
            urls = get_multi_pages_turnbackhoax(config)

        save_url_temp(urls)

    get_multi_news_content(config, urls)
    remove_url_temp()
    remove_temp_progress()


def run_cnn(num_of_page: int):
    print('Starting CNN News Scrapper')
    config = CNNConfig(num_of_page)
    run(config)


def run_kompas(num_of_page: int):
    print('Starting Kompas News Scrapper')
    config = KompasConfig(num_of_page)
    run(config)


def run_tempo(num_of_day: int, start_date:str='2022-01-01'):
    print('Starting Tempo News Scrapper')
    config = TempoConfig(num_of_day, start_date)
    run(config)


def run_turnbackhoax(num_of_page: int):
    print('Starting Turnbackhoax.id News Scrapper')
    config = TurnbackhoaxConfig(num_of_page)
    run(config)