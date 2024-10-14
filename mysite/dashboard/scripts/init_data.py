# 해당 코드 shell에서 실행을 통한 초기 데이터 설정
# from dashboard.scripts.init_data import Command
# cmd = Command()
# cmd.handle()

from django.core.management.base import BaseCommand
import csv
from dashboard.models import Recipe, Ingredient, RecipeOrder  # 'dashboard'를 실제 앱 이름으로 변경하세요.

class Command(BaseCommand):
    help = 'Initialize data from CSV file'

    def handle(self, *args, **options):
        # CSV 파일의 절대 경로를 설정합니다.
        csv_file_path = '/Users/juho/Documents/recipe/new-recipe/무제/base_data.csv'

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 헤더를 건너뜁니다.

            for row in reader:
                if len(row) != 7:  # 데이터가 정확히 7개 열인지 확인
                    self.stdout.write(self.style.ERROR('Invalid row: %s' % row))
                    continue

                recipe_title = row[0]
                link = row[1]
                servings = row[2]  # servings 데이터
                time = row[3]      # time 데이터
                image_url = row[4]
                ingredients = eval(row[5])  # 문자열을 리스트로 변환
                orders = eval(row[6])  # 문자열을 리스트로 변환

                # 레시피 생성
                recipe = Recipe.objects.create(
                    recipe_title=recipe_title,
                    link=link,
                    servings=servings,  # servings 필드 추가
                    time=time,          # time 필드 추가
                    image_url=image_url
                )

                # 재료 생성
                for ingredient in ingredients:
                    Ingredient.objects.create(recipe=recipe, ingredient=ingredient)

                # 조리 순서 생성
                for order in orders:
                    RecipeOrder.objects.create(recipe=recipe, order=order)

                self.stdout.write(self.style.SUCCESS('Successfully added recipe: %s' % recipe_title))
