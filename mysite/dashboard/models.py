from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_title = models.CharField(max_length=200, verbose_name='레시피명')
                                  
    def __str__(self):
        return f'레시피: {self.recipe}'

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=200, verbose_name='재료')
    
    def __str__(self):
        return self.ingredient

    