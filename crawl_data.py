import requests
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup

# 레시피 랭킹 페이지 링크
link = 'https://m.10000recipe.com/ranking/home_view.html?dtype=m&rtype=r'

# 전체 데이터 요청
data = requests.get(link)
soup = BeautifulSoup(data.text, 'html.parser')

# 레시피 제목을 담고 있는 div 찾기
line = soup.find_all('div', class_='common_rcp_caption_tit line2')

# 데이터 저장을 위한 DataFrame 생성
link_base = 'https://m.10000recipe.com/'
df = pd.DataFrame(line, columns=['data'])

# 레시피 링크 생성
for idx, val in enumerate(line):
    df.loc[idx, 'link'] = link_base + val['onclick'].replace("location.href='/", '').replace("'", '')

# 개별 페이지 크롤링
for idx in tqdm(range(len(df))):
    link = df.loc[idx, 'link']
    data = requests.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    # 재료 추출
    ingredient_items = soup.find('dl', class_='view3_ingre').find_all('li')
    ingredients = str(list(map(lambda x: x.find('div', 'ingre_list_name').text.strip(), ingredient_items)))
    df.loc[idx, 'ingredient'] = ingredients

    # 요리 단계 추출
    steps = soup.find_all('li', id=lambda x: x and x.startswith('stepDiv'))  # 'stepDiv'로 시작하는 li 태그 찾기
    step_descriptions = []
    for step in steps:
        step_text = step.find('div', class_='step_list_txt_cont')
        if step_text:
            step_descriptions.append(step_text.get_text(strip=True).replace('\n', ' '))

    if step_descriptions:
        df.loc[idx, 'orders'] = str(step_descriptions)  # 요리 단계를 DataFrame에 저장
    else:
        df.loc[idx, 'orders'] = "단계 없음"  # 단계가 없을 경우 처리

# CSV 파일로 저장
df.to_csv('base_data.csv', index=False, encoding='utf-8-sig')
print("데이터를 CSV 파일로 저장했습니다: base_data.csv")



df.columns = ['recipe_title', 'link', 'ingredients', 'recipe_orders']

df['ingredients'] = df['ingredients'].apply(lambda x : eval(x))
df['recipe_orders'] = df['recipe_orders'].apply(lambda x : eval(x))

df['ingredients'] = df['ingredients'].apply(lambda x : ["{'ingredient' : '"+ str(i) + "'}" for i in x])
df['recipe_orders'] = df['recipe_orders'].apply(lambda x : ["{'order' : '"+ str(i) + "'}" for i in x])


line = df.loc[0].to_json()

# 여기서 for문 돌면 되지 않을까요?
import json
json.loads(line)
