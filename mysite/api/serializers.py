from rest_framework import serializers
from dashboard.models import Recipe, Ingredient, RecipeOrder

# I
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient']


class RecipeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeOrder
        fields = ['order']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    recipe_orders = RecipeOrderSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'recipe_title', 'link', 'time', 'servings', 'ingredients', 'recipe_orders']
    
    # list input 처리
    def create(self, validated_data):
        # ingredients, recipe_orders, recipe_link 데이터를 분리
        ingredients_data = validated_data.pop('ingredients')
        recipe_orders = validated_data.pop('recipe_orders')
        
        # Recipe 생성
        recipe = Recipe.objects.create(**validated_data)  

        # 각 Ingredient를 생성하여 Recipe와 연결
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        
        # 각 recipe_orders를 Recipe와 연결
        for recipe_order in recipe_orders:
            RecipeOrder.objects.create(recipe=recipe, **recipe_order)

        return recipe
