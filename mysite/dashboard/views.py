from django.shortcuts import render
from django.http import HttpResponse 
import json
from . import models
from collections import Counter

# Create your views here.
def index(request):
    most_popular_ingredient = Counter([i.ingredient for i in models.Ingredient.objects.all()]).most_common(6)
    most_popular_ingredient_name = [name for name, val in most_popular_ingredient]
    most_popular_ingredient_amount = [val for name, val in most_popular_ingredient]
    
    context = {'most_popular_ingredient_name': json.dumps(most_popular_ingredient_name),
               'most_popular_ingredient_amount' : json.dumps(most_popular_ingredient_amount),
               }
    return render(request, 'index.html', context)
    