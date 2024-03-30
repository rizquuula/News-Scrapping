from NewsScraper.models.base_url import BaseUrl
from NewsScraper.utils import get_timestamp
from .scraper_config import ScraperConfig


class CNNConfig(ScraperConfig):
    def __init__(
        self,
        num_of_page: int,
        output_dir: str,
        filename: str,
        overwrite: bool=True,
        ):
        super().__init__(
            BaseUrl.CNN,
            filename=filename,
            num_of_page=num_of_page,
            output_dir=output_dir,
            overwrite=overwrite,
        )


class KompasConfig(ScraperConfig):
    def __init__(
        self,
        num_of_page: int,
        output_dir: str,
        filename: str,
        overwrite: bool=True,
        ):
        super().__init__(
            BaseUrl.Kompas,
            filename=filename,
            num_of_page=num_of_page,
            output_dir=output_dir,
            overwrite=overwrite,
        )


class TempoConfig(ScraperConfig):
    def __init__(
        self, 
        num_of_page: int,
        start_date: str,
        output_dir: str,
        filename: str,
        overwrite: bool=True,
        ):
        super().__init__(
            BaseUrl.Tempo   ,
            filename=filename,
            num_of_page=num_of_page,
            start_date=start_date,
            output_dir=output_dir,
            overwrite=overwrite,
        )


class TurnbackhoaxConfig(ScraperConfig):
    def __init__(
        self,
        num_of_page: int,
        output_dir: str,
        filename: str,
        overwrite: bool=True,
        ):
        super().__init__(
            BaseUrl.Turnbackhoax,
            filename=filename,
            num_of_page=num_of_page,
            output_dir=output_dir,
            overwrite=overwrite,
        )
        