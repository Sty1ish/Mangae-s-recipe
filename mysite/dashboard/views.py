from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse 
from mysite import settings
from .models import *
from collections import Counter
import json
import pandas as pd
import random

def visual_detail(request):
    recipes = Recipe.objects.all()
    
    ingredients = Ingredient.objects.all()
    ingredient_counts = Counter(ingredient.ingredient for ingredient in ingredients)

    top_ingredients = ingredient_counts.most_common()
    labels = [ingredient[0] for ingredient in top_ingredients]
    data = [ingredient[1] for ingredient in top_ingredients]

    # 요리 시간 구하기
    cook_time = (pd.cut(pd.Series([i.time for i in Recipe.objects.all()]), [-1, 10, 20, 30, 60, 90, 121])
                 .value_counts()
                 .sort_index()
                 .reset_index()
                 )
    cook_time.loc[:, 'index'] = ['10분 미만', '10~20분', '20~30분', '30~60분', '60~90분', '90~120분']
    
    # 랜덤 레시피 선택
    random_recipe = random.choice(recipes) if recipes else None

    return render(request, 'visual_detail.html', {
        'recipes': recipes,
        'random_recipe': random_recipe,
        'labels_json': json.dumps(labels, ensure_ascii=False),
        'data_json': json.dumps(data),
        'ingredients_json': json.dumps([{'name': name, 'frequency': freq} for name, freq in top_ingredients], ensure_ascii=False),
        'cook_time_label': cook_time['index'].tolist(),
        'cook_time_data': cook_time['count'].tolist(),
    })

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    orders_with_index = enumerate([i.order for i in recipe.recipe_orders.all()])
    
    # 추천 상품 구하기
    def get_random_recipe():
        return Recipe.objects.order_by("?").first()
    
    random_recipe = [get_random_recipe() for _ in range(4)]
    
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'orders_with_index' : orders_with_index,
        'random_recipe' : random_recipe,
        })

def recipe_list(request):
    recipes = Recipe.objects.all()
    
    # 재료 빈도수 계산
    ingredients = Ingredient.objects.all()
    ingredient_counts = Counter(ingredient.ingredient for ingredient in ingredients)
    
    # 가장 빈도가 높은 15개 재료 가져오기
    top_ingredients = ingredient_counts.most_common(20)
    labels = [ingredient[0] for ingredient in top_ingredients]
    data = [ingredient[1] for ingredient in top_ingredients]

    # 요리 시간 구하기
    cook_time = (pd.cut(pd.Series([i.time for i in Recipe.objects.all()]), [-1, 10,20,30,60,90,121])
                 .value_counts()
                 .sort_index()
                 .reset_index()
                 )
    cook_time.loc[:, 'index'] = ['10분 미만', '10~20분', '20~30분', '30~60분', '60~90분', '90~120분']

    return render(request, 'index.html', {
        'recipes': recipes,
        'labels_json': json.dumps(labels, ensure_ascii=False),
        'data_json': json.dumps(data),
        'ingredients_json': json.dumps([{'name': name, 'frequency': freq} for name, freq in top_ingredients], ensure_ascii=False),
        'cook_time_label' : cook_time['index'].tolist(),
        'cook_time_data' : cook_time['count'].tolist(),
    })
    
def chart_search_list(request, search_type, chart_label):
    # 요리 시간 구하기 (dataFrame 인덱스를 기준으로 필터링)
    cook_time = pd.DataFrame([i.time for i in Recipe.objects.all()], columns = ['time']) 
    cook_time['time_split'] = pd.cut(cook_time['time'], [-1, 10,20,30,60,90,121])
    mapping_dict = {i : v for i, v in zip(cook_time['time_split'].value_counts().sort_index().index, ['10분 미만', '10~20분', '20~30분', '30~60분', '60~90분', '90~120분'])}
    cook_time['time_split_mapping'] = cook_time['time_split'].apply(lambda x : mapping_dict[x])
    
    # 재료 매핑
    cook_time['isin_ingredient'] = [len(i.ingredients.all().filter(ingredient__icontains=chart_label)) != 0 for i in Recipe.objects.all()]
    
    if search_type == 'time':
        search_result_recipe = [obj for idx, obj in enumerate(Recipe.objects.all()) if idx in cook_time[cook_time['time_split_mapping'] == chart_label].index.tolist()]
    elif search_type == 'ingredient':
        search_result_recipe = [obj for idx, obj in enumerate(Recipe.objects.all()) if idx in cook_time[cook_time['isin_ingredient'] == True].index.tolist()]
    else:
        search_result_recipe = None
    
    return render(request, 'serach_result.html', {
        'search_result_recipe' : search_result_recipe,
        'search_type' : search_type,
        'chart_label' : chart_label
    })