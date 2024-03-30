from typing import Type
from NewsScraper.config.config_factory import CNNConfig, KompasConfig, TempoConfig, TurnbackhoaxConfig
from NewsScraper.config.scraper_config import ScraperConfig
from NewsScraper.scraper.cnn_scraper import CNNScraper
from NewsScraper.scraper.kompas_scraper import KompasScraper
from NewsScraper.scraper.scraper import Scraper
from NewsScraper.scraper.tempo_scraper import TempoScraper
from NewsScraper.scraper.turnbackhoax_scraper import TurnbackhoaxScraper
from NewsScraper.scraper_data.scraper_data import ScraperData
from NewsScraper.scraper_url.scraper_url import ScraperUrl
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress


def execute_scrapper(
    config: ScraperConfig,
    scraper_class: Type[Scraper],
) -> ScraperData:
    progress = ScraperProgress(
        filename=config.filename
    )
    
    news_url = ScraperUrl()
    
    data = ScraperData(
        output_dir=config.output_dir,
        filename=config.filename,
    )
    
    scraper = scraper_class(
        config=config,
        progress=progress,
        news_url=news_url,
        dataset=data,
    )
    scraper_data = scraper.run_scraper()
    return scraper_data


def scrap_cnn(
    num_of_page: int,
    output_filename: str,
    overwrite: bool=False,
    output_dir: str='dataset',
) -> ScraperData:
    config = CNNConfig(
        num_of_page=num_of_page,
        output_dir=output_dir,
        filename=output_filename,
        overwrite=overwrite,
    )
    scraper_data = execute_scrapper(config, CNNScraper)
    return scraper_data


def scrap_kompas(
    num_of_page: int,
    output_filename: str,
    overwrite: bool=False,
    output_dir: str='dataset',
) -> ScraperData:
    config = KompasConfig(
        num_of_page=num_of_page,
        output_dir=output_dir,
        filename=output_filename,
        overwrite=overwrite,
    )
    scraper_data = execute_scrapper(config, KompasScraper)
    return scraper_data


def scrap_tempo(
    num_of_page: int,
    start_date: str,
    output_filename: str,
    overwrite: bool=False,
    output_dir: str='dataset',
) -> ScraperData:
    config = TempoConfig(
        num_of_page=num_of_page,
        start_date=start_date,
        output_dir=output_dir,
        filename=output_filename,
        overwrite=overwrite,
    )
    scraper_data = execute_scrapper(config, TempoScraper)
    return scraper_data


def scrap_turnbackhoax(
    num_of_page: int,
    output_filename: str,
    overwrite: bool=False,
    output_dir: str='dataset',
) -> ScraperData:
    config = TurnbackhoaxConfig(
        num_of_page=num_of_page,
        output_dir=output_dir,
        filename=output_filename,
        overwrite=overwrite,
    )
    scraper_data = execute_scrapper(config, TurnbackhoaxScraper)
    return scraper_data