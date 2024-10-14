from rest_framework import serializers
from dashboard.models import Recipe, Ingredient, RecipeOrder, RecipeLink

# I
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['recipe']
        
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['recipe', 'ingredient']

class RecipeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeOrder
        fields = ['recipe', 'recipe_order']

class RecipeLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLink
        fields = ['recipe', 'recipe_link']