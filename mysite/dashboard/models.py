from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_title = models.CharField(max_length=200, verbose_name='레시피명')
                                
    def __str__(self):
        return f'레시피: {self.recipe}'

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='Ingredients', on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=200, verbose_name='재료')
    
    def __str__(self):
        return self.ingredient

class RecipeOrder(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_orders', on_delete=models.CASCADE)
    order = models.CharField(max_length=500, verbose_name='레시피 순서')

    def __str__(self):
        return f'{self.recipe} : {self.order}'
    
class RecipeLink(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_link', on_delete=models.CASCADE)
    link = models.CharField(max_length=200, verbose_name='레시피 링크')

    def __str__(self):
        return self.link