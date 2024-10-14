from django.db import models

class Recipe


# Create your models here.
class Recipe(models.Model):
    recipe = models.CharField(max_length=200, verbose_name='레시피명')
                                  
    def __str__(self):
        return f'레시피: {self.question_text}'

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete='확인필요')
    ingredient = models.CharField(max_length=200, verbose_name='재료')
    
    def __str__(self):
        return self.ingredient

    