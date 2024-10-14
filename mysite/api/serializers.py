from rest_framework import serializers
from dashboard.models import Recipe, Ingredient

# I
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['recipe']
        
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['recipe', 'ingredient']