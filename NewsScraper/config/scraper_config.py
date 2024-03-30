import os
from typing import Optional

from NewsScraper.scraper_progress.scraper_progress import ScraperProgress


class ScraperConfig:
    def __init__(
        self,
        base_url: str,
        filename: str,
        overwrite: bool=True,
        output_dir: str=None,
        start_date: Optional[str]=None,
        num_of_page: Optional[int]=None,
    ) -> None:
        self.base_url = base_url
        self.filename = filename
        
        self.overwrite = overwrite
        self.output_dir = output_dir
        self.start_date = start_date
        self.num_of_page = num_of_page
        
        self.__create_output_dir()

    def __create_output_dir(self):
        try:
            if not os.path.isdir(self.output_dir):
                os.mkdir(self.output_dir)
                return self.output_dir
        except Exception as e:
            raise Exception(f'Fail to create new dir. {e}')
