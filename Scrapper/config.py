import os
from Scrapper.obj import Progress
from Scrapper.utils import get_timestamp

TEMP_URL_CSV = '__temp_url.csv'
TEMP_PROGRESS = '__temp_progress.csv'
DELIMITER_CSV = ';'


class BaseUrl(object):
    CNN = 'https://www.cnnindonesia.com/politik/indeks/4/'
    Kompas = 'https://www.kompas.com/tag/politik'
    Tempo = 'https://www.tempo.co/indeks/YYYY-MM-DD/nasional/politik'
    Turnbackhoax = 'https://turnbackhoax.id'


class Config:
    def __init__(self):
        self.BASE_URL = None
        self.FILENAME = None
        self.OUTPUT_DIR = os.getcwd() + '/dataset'
        self.LAST_ID = 0
        self._check_dir()

    def update_by_progress(self, progress: Progress):
        if progress:
            self.FILENAME = progress.Filename
            self.LAST_ID = progress.LastId

    def _check_dir(self):
        if not os.path.isdir(self.OUTPUT_DIR):
            os.mkdir(self.OUTPUT_DIR)


class CNNConfig(Config):
    def __init__(self, num_of_page):
        super().__init__()
        self.BASE_URL=BaseUrl.CNN
        self.FILENAME=f'dataset_cnn_{get_timestamp()}.csv'
        self.NUM_OF_PAGE = num_of_page


class KompasConfig(Config):
    def __init__(self, num_of_page):
        super().__init__()
        self.BASE_URL=BaseUrl.Kompas
        self.FILENAME=f'dataset_kompas_{get_timestamp()}.csv'
        self.NUM_OF_PAGE = num_of_page


class TempoConfig(Config):
    def __init__(self, num_of_day, start_date):
        super().__init__()
        self.BASE_URL=BaseUrl.Tempo
        self.FILENAME=f'dataset_tempo_{get_timestamp()}.csv'
        self.START_DATE=start_date
        self.NUM_OF_DAY=num_of_day


class TurnbackhoaxConfig(Config):
    def __init__(self, num_of_page):
        super().__init__()
        self.BASE_URL=BaseUrl.Turnbackhoax
        self.FILENAME=f'dataset_turnbackhoax_{get_timestamp()}.csv'
        self.NUM_OF_PAGE = num_of_page