import requests
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup

link = 'https://m.10000recipe.com/ranking/home_view.html?dtype=m&rtype=r'

data = requests.get(link)

soup = BeautifulSoup(data.text, 'html.parser')

line = soup.find_all('div', class_ = 'common_rcp_caption_tit line2')


# data Save
link_base = 'https://m.10000recipe.com/'

df = pd.DataFrame(line, columns = ['data'])
for idx, val in enumerate(line):
    df.loc[idx, 'link'] = link_base + val['onclick'].replace("location.href='/",'').replace("'", '')



# 개별 페이지 크롤링

link = 'https://m.10000recipe.com/recipe/6845428'

data = requests.get(link)

soup = BeautifulSoup(data.text, 'html.parser')


for idx in tqdm(range(len(df))):
    link = df.loc[idx, 'link']
    data = requests.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
    df.loc[idx, 'ingredient'] = str(list(map(lambda x : x.find('a').text.strip(), soup.find('dl', class_ = 'view3_ingre').find_all('li'))))


df.to_csv('base_data.csv', index = False)
