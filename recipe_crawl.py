import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

csv_file_path = '/Users/juho/crwal_test/만개의레시피_Top_100.csv'
base_url = 'https://www.10000recipe.com/recipe/'

def load_csv(file_path):
    links = []
    with open(file_path, newline='', encoding='euc-kr') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            links.append(row['레시피링크'])
    print(f"총 {len(links)}개의 레시피 링크를 로드했습니다.")  # 링크 개수 확인
    return links

def page_crawler(recipe_url):
    print(f"크롤링 중: {recipe_url}")
    page = requests.get(recipe_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    steps = []
    
    try:
        # 요리 단계를 담고 있는 div를 찾기
        res = soup.find('div', 'view_step')
        if not res:
            print(f"Warning: {recipe_url}에서 view_step을 찾을 수 없습니다.")
            return None

        # 요리 단계를 반복하여 추출
        step_items = res.find_all('div', 'view_step_cont')
        for i, n in enumerate(step_items, start=1):
            step_desc = n.get_text(strip=True).replace('\n', ' ')
            steps.append({
                'Step': f"#{i}",
                'Description': step_desc
            })
            print(f"STEP #{i}: {step_desc}")  # 각 단계 출력

    except AttributeError as e:
        print(f"Error parsing {recipe_url}: {e}")
        return None

    return steps


def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"데이터를 엑셀 파일로 저장했습니다: {output_file}")

def crawl_recipes(links):
    all_recipes = []
    
    for link in links:
        recipe_steps = page_crawler(link)
        if recipe_steps:
            for step in recipe_steps:
                step['Recipe_URL'] = link  # 레시피 링크 추가
                all_recipes.append(step)
    
    print(f"총 {len(all_recipes)}개의 레시피 데이터를 수집했습니다.")  # 수집된 데이터 확인
    return all_recipes

# CSV에서 링크 불러오기
recipe_links = load_csv(csv_file_path)

# 모든 레시피 크롤링
recipe_data = crawl_recipes(recipe_links)

# 엑셀 파일로 저장
output_file = '/Users/juho/crwal_test/만개의레시피_Top_100_test.xlsx'
save_to_excel(recipe_data, output_file)