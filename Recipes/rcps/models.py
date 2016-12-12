from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe_rating = models.FloatField(default=0)
    recipe_link = models.URLField(max_length=500)
    commentators = models.ManyToManyField(User, through='Comment', related_name='commentators')
    graders = models.ManyToManyField(User, through='Grade', related_name='graders')

    def __str__(self):

        return self.recipe_name


class EquipmentCategory(models.Model):
    ecategory_name = models.CharField(max_length=200)

    def __str__(self):
        return self.ecategory_name


class Equipment(models.Model):
    equipment_name = models.CharField(max_length=200)
    equipment_category = models.ForeignKey(EquipmentCategory)
    alternatives = models.ManyToManyField('self', blank=True)
    equipment_recipes = models.ManyToManyField(Recipe, through='Requires')

    def __str__(self):
        return self.equipment_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    tag_recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.tag_name


class IngredientCategory(models.Model):
    icategory_name = models.CharField(max_length=200)

    def __str__(self):
        return self.icategory_name


class Ingredient(models.Model):
    ingredient_category = models.ForeignKey(IngredientCategory)
    ingredient_name = models.CharField(max_length=200)
    recipes = models.ManyToManyField(Recipe, through='Consist')

    def __str__(self):
        return self.ingredient_name


class IngredientAlternative(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='AlternativeConsists', related_name='ingredients')


    def __str__(self):
        return ', '.join((x[0] for x in self.ingredients.values_list('ingredient_name')))


class AlternativeConsists(models.Model):
    ingredient_alternative = models.ForeignKey(IngredientAlternative)
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.CharField(max_length=200)


class Consist(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.CharField(max_length=200)

    def __str__(self):
        return self.ingredient.ingredient_name + ' в ' + self.recipe.recipe_name


class IngredientReplacement(models.Model):
    ingredient_entry = models.ForeignKey(Consist)
    alternative = models.ForeignKey(IngredientAlternative)
    alternative_quality = models.IntegerField()

    def __str__(self):
        recipe_name = self.ingredient_entry.recipe.__str__()
        ingredient_name =  self.ingredient_entry.ingredient.__str__()
        return ingredient_name + ' в ' + recipe_name + ' на ' + self.alternative.__str__()


class Comment(models.Model):
    comment_author = models.ForeignKey(User)
    comment_recipe = models.ForeignKey(Recipe)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)


class Grade(models.Model):
    grade_stars = models.IntegerField()
    grade_favorite = models.BooleanField(default=False)
    grader = models.ForeignKey(User)
    grade_recipe = models.ForeignKey(Recipe)


class Requires(models.Model):
    recipe = models.ForeignKey(Recipe)
    equipment = models.ForeignKey(Equipment)
