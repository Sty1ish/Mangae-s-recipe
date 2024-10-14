from rest_framework import serializers
from dashboard.models import Recipe, Ingredient, RecipeOrder, RecipeLink

# I
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'recipe_title', 'ingredients']
    
    # list input 처리
    def create(self, validated_data):
        # 중첩된 ingredients 데이터를 분리
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)  # Recipe 생성

        # 각 Ingredient를 생성하여 Recipe와 연결
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        
        return recipe


class RecipeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeOrder
        fields = ['recipe', 'recipe_order']

class RecipeLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLink
        fields = ['recipe', 'recipe_link']