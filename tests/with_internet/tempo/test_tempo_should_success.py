import csv
import os
from NewsScraper import scrap_tempo
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress
from NewsScraper.scraper_url.scraper_url import ScraperUrl


def test_tempo_should_success():
    data = scrap_tempo(
        num_of_page=1,
        start_date='2022-01-01',
        output_filename='tempo.csv',
        overwrite=True
    )
    
    assert len(data.data) != 0
    assert data.filename == 'tempo.csv'
    
    # remove output file
    data.delete_data()


def test_tempo_should_success_continue_temp():
    filename = 'tempo.csv'
    output_dir = 'dataset'
    with open(os.path.join(output_dir, filename), 'w') as f:
        w = csv.writer(f)
    
    all_links = [
        'https://nasional.tempo.co/read/1545504/maruf-amin-akan-saksikan-lagi-timnas-indonesia-vs-thailand-di-final-aff-2020',
        'https://nasional.tempo.co/read/1545477/menag-yaqut-canangkan-2022-sebagai-tahun-toleransi',
        'https://nasional.tempo.co/read/1545437/jokowi-ajak-masyarakat-hadapi-2022-dengan-semangat-baru',
        'https://nasional.tempo.co/read/1545377/top-nasional-strategi-hadapi-omicron-lemhanas-usul-bentuk-kementerian-baru',
        'https://nasional.tempo.co/read/1545310/mulai-tahun-ini-menteri-tjahjo-kumolo-minta-pns-apel-pagi-tiap-senin',
    ]
    progress = ScraperProgress(
        filename=filename
    )
    
    news_url = ScraperUrl()
    
    news_url.save_url_temp(all_links)
    progress.update_progress(3)
    
    data = scrap_tempo(
        num_of_page=1,
        start_date='2022-01-01',
        output_filename=filename,
        overwrite=False
    )
    
    assert len(data.data) != 0
    assert data.filename == filename
    
    # remove output file
    data.delete_data()
    