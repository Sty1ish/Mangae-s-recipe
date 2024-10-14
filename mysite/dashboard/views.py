from django.shortcuts import render
from django.http import HttpResponse 
import json
from .models import *
from collections import Counter

# Create your views here.
def index(request):
    most_popular_ingredient = Counter([i.ingredient for i in Ingredient.objects.all()]).most_common(6)
    most_popular_ingredient_name = [name for name, val in most_popular_ingredient]
    most_popular_ingredient_amount = [val for name, val in most_popular_ingredient]
    
    context = {'most_popular_ingredient_name': json.dumps(most_popular_ingredient_name),
               'most_popular_ingredient_amount' : json.dumps(most_popular_ingredient_amount),
               }
    return render(request, 'index.html', context)

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

    return render(request, 'index.html', {
        'recipes': recipes,
        'labels': labels,
        'data': data,
    })
