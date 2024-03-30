import csv
import os
from NewsScraper.static_vars import *


class ScraperProgress:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.last_id = 0

    def read_progress(self):
        if self.is_temp_progress_exists():
            with open (TEMP_PROGRESS, 'r') as f:
                reader = csv.reader(f, delimiter=DELIMITER_CSV)
                data = list(reader)[0]
                self.filename = data[0]
                self.last_id = int(data[1])

    def update_progress(self, last_id) -> None:
        self.last_id = last_id
        self.__save_progress_to_file()

    def is_temp_progress_exists(self):
        return os.path.isfile(TEMP_PROGRESS)
    
    def delete_progress(self):
        if self.is_temp_progress_exists():
            os.remove(TEMP_PROGRESS)

    def __save_progress_to_file(self) -> None:
        with open(TEMP_PROGRESS, 'w') as f:
            writer = csv.writer(f, delimiter=DELIMITER_CSV)
            writer.writerow([self.filename, self.last_id])
