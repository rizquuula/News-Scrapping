import os
from Scrapper.utils import get_timestamp

TEMP_URL_CSV = '__temp_url.csv'
DELIMITER_CSV = ';'


class BaseUrl(object):
    CNN = 'https://www.cnnindonesia.com/politik/indeks/4/'
    Kompas = 'https://www.kompas.com/tag/politik'
    Tempo = 'https://www.tempo.co/indeks/2023-02-01/nasional/politik'


class Config:
    def __init__(self):
        self.BASE_URL = None
        self.FILENAME = None
        self.OUTPUT_DIR = os.getcwd() + '/dataset'
        self._check_dir()

    def _check_dir(self):
        if not os.path.isdir(self.OUTPUT_DIR):
            os.mkdir(self.OUTPUT_DIR)


class CNNConfig(Config):
    def __init__(self):
        super().__init__()
        self.BASE_URL=BaseUrl.CNN
        self.FILENAME=f'dataset_cnn_{get_timestamp()}.csv'


class KompasConfig(Config):
    def __init__(self):
        super().__init__()
        self.BASE_URL=BaseUrl.Kompas
        self.FILENAME=f'dataset_kompas_{get_timestamp()}.csv'


class TempoConfig(Config):
    def __init__(self):
        super().__init__()
        self.BASE_URL=BaseUrl.Tempo
        self.FILENAME=f'dataset_tempo_{get_timestamp()}.csv'

