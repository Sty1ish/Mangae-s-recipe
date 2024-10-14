from django.urls import path, include
from .views import *

app_name = 'api'

urlpatterns = [
    path('recipe/', RecipeList.as_view(), name='recipe-list'),
    path('recipe/<int:pk>', RecipeDetail.as_view(), name='recipe-detail'),
]