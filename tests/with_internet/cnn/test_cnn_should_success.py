import csv
import os
from NewsScraper import scrap_cnn
from NewsScraper.models.base_url import BaseUrl
from NewsScraper.scraper_progress.scraper_progress import ScraperProgress
from NewsScraper.scraper_url.scraper_url import ScraperUrl


def test_cnn_should_success():
    data = scrap_cnn(
        base_url=BaseUrl.indo_cnn.politik,
        num_of_page=1,
        output_filename='cnn.csv',
        overwrite=True
    )
    
    assert len(data.data) != 0
    assert data.filename == 'cnn.csv'
    
    # remove output file
    data.delete_data()
    

def test_cnn_should_success_continue_temp():
    filename = 'cnn.csv'
    output_dir = 'dataset'
    with open(os.path.join(output_dir, filename), 'w') as f:
        w = csv.writer(f)
    
    all_links = [
        'https://www.cnnindonesia.com/nasional/20240331024920-32-1080833/pdip-waspadai-operasi-politik-revisi-uu-md3-2014-habiskan-us-3-juta',
        'https://www.cnnindonesia.com/nasional/20240330162117-32-1080754/sekjen-pdip-akui-khilaf-pernah-dukung-gibran-jadi-wali-kota-solo',
        'https://www.cnnindonesia.com/nasional/20240329201501-32-1080577/airlangga-klaim-belum-ada-upaya-dekati-partai-dpr-demi-revisi-uu-md3',
        'https://www.cnnindonesia.com/nasional/20240329195117-32-1080575/airlangga-soal-jadi-saksi-sidang-pilpres-di-mk-belum-ada-undangan',
        'https://www.cnnindonesia.com/nasional/20240329192215-32-1080572/prabowo-di-depan-airlangga-kita-timnya-jokowi',
    ]
    progress = ScraperProgress(
        filename=filename
    )
    
    news_url = ScraperUrl()
    
    news_url.save_url_temp(all_links)
    progress.update_progress(3)
    
    data = scrap_cnn(
        base_url=BaseUrl.indo_cnn.politik,
        num_of_page=1,
        output_filename=filename,
        overwrite=False
    )
    
    assert len(data.data) != 0
    assert data.filename == filename
    
    # remove output file
    data.delete_data()
    