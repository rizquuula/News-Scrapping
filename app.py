from NewsScraper import scrap_cnn, scrap_kompas, scrap_tempo, scrap_turnbackhoax


scrap_kompas(
    num_of_page=2,
    output_filename='kompas.csv',
    overwrite=False
)

# scrap_cnn(
#     num_of_page=2,
#     output_filename='cnn.csv',
#     overwrite=False
# )

# scrap_tempo(
#     num_of_page=2,
#     start_date='2022-01-01',
#     output_filename='tempo.csv',
#     overwrite=False
# )

## Fail due to captcha
# scrap_turnbackhoax(
#     num_of_page=2,
#     output_filename='turnbackhoax.csv',
#     overwrite=False
# )