from NewsScraper import scrap_cnn, scrap_kompas, scrap_tempo, scrap_turnbackhoax
from NewsScraper.models.base_url import BaseUrl


scrap_kompas(
    base_url=BaseUrl.kompas.politik,
    num_of_page=2,
    output_filename='kompas.csv',
    overwrite=False
)

# scrap_cnn(
#     base_url=BaseUrl.indo_cnn.politik,
#     num_of_page=2,
#     output_filename='cnn.csv',
#     overwrite=True
# )

# scrap_tempo(
#     base_url=BaseUrl.tempo.politik,
#     num_of_page=2,
#     start_date='2022-01-01',
#     output_filename='tempo.csv',
#     overwrite=False
# )

## Fail due to captcha
# scrap_turnbackhoax(
#     base_url=BaseUrl.turnbackhoax.index,
#     num_of_page=2,
#     output_filename='turnbackhoax.csv',
#     overwrite=False
# )