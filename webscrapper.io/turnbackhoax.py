import pandas as pd

csv_url = '/Users/rizquuula/Playground/News-Scrapping/webscrapper.io/turnbackhoax-news-url.csv'

df_tbh = pd.read_csv(csv_url)
links = df_tbh['news-link-href'].values

with open('temp.txt', 'w') as f:
    txt = ''
    for link in links:
        txt += f'"{link}",'
    f.write(txt)