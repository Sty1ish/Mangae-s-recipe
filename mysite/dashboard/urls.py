from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('visual/', views.visual_detail, name='visual')
]
