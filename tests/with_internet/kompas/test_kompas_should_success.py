import csv
import os
from NewsScraper import scrap_kompas
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress
from NewsScraper.scraper_url.scraper_url import ScraperUrl


def test_kompas_should_success():
    data = scrap_kompas(
        num_of_page=1,
        output_filename='kompas.csv',
        overwrite=True
    )
    
    assert len(data.data) != 0
    assert data.filename == 'kompas.csv'
    
    # remove output file
    data.delete_data()
    

def test_kompas_should_success_continue_temp():
    filename = 'kompas.csv'
    output_dir = 'dataset'
    with open(os.path.join(output_dir, filename), 'w') as f:
        w = csv.writer(f)
    
    all_links = [
        'https://video.kompas.com/watch/1347546/prabowo-kita-timnya-pak-jokowi-harus-perangi-korupsi',
        'https://video.kompas.com/watch/1347538/prabowo-akan-bertemu-presiden-china-xi-jinping',
        'http://nasional.kompas.com/read/2024/03/30/10582711/kubu-ganjar-mahfud-optimistis-mk-jawab-kebuntuan-politik-dan-hukum',
        'https://video.kompas.com/watch/1347283/gibran-dampingi-prabowo-ke-bukber-golkar-absen-saat-bareng-pan-dan-demokrat',
        'https://video.kompas.com/watch/1347266/prabowo-gibran-menang-pilpres-siapa-tergiur-masuk-koalisi-dan-siapa-siap-oposisi',
    ]
    progress = ScraperProgress(
        filename=filename
    )
    
    news_url = ScraperUrl()
    
    news_url.save_url_temp(all_links)
    progress.update_progress(3)
    
    data = scrap_kompas(
        num_of_page=1,
        output_filename=filename,
        overwrite=False
    )
    
    assert len(data.data) != 0
    assert data.filename == filename
    
    # remove output file
    data.delete_data()
    