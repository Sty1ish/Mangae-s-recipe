from rest_framework import serializers
from dashboard.models import Recipe, Ingredient, RecipeOrder, RecipeLink

# I
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient']

class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'recipe_title', 'ingredient']


class RecipeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeOrder
        fields = ['recipe', 'recipe_order']

class RecipeLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLink
        fields = ['recipe', 'recipe_link']