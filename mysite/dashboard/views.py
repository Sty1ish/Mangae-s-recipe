from django.shortcuts import render
from django.http import HttpResponse 
import json
from .models import *
from collections import Counter
import pandas as pd

def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def recipe_list(request):
    recipes = Recipe.objects.all()
    
    # 재료 빈도수 계산
    ingredients = Ingredient.objects.all()
    ingredient_counts = Counter(ingredient.ingredient for ingredient in ingredients)
    
    # 가장 빈도가 높은 15개 재료 가져오기
    top_ingredients = ingredient_counts.most_common(15)
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
        'labels': labels,
        'data': data,
        'cook_time_label' : cook_time['index'].tolist(),
        'cook_time_data' : cook_time['count'].tolist(),
    })
