from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe_rating = models.FloatField()
    recipe_link = models.URLField(max_length=500)
    commentators = models.ManyToManyField(User, through='Comment', related_name='commentators')
    graders = models.ManyToManyField(User, through='Grade', related_name='graders')


class EquipmentCategory(models.Model):
    ecategory_name = models.CharField(max_length=200)


class Equipment(models.Model):
    equipment_name = models.CharField(max_length=200)
    equipment_category = models.ForeignKey(EquipmentCategory)
    equipment_alternative = models.ForeignKey('Equipment')
    equipment_recipes = models.ManyToManyField(Recipe)


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    tag_recipes = models.ManyToManyField(Recipe)


class IngredientCategory(models.Model):
    icategory_name = models.CharField(max_length=200)


class IngredientAlternative(models.Model):
    alternative_recipe = models.ForeignKey(Recipe)
    alternative_quality = models.IntegerField()


class Ingredient(models.Model):
    ingredient_category = models.ForeignKey(IngredientCategory)
    ingredient_name = models.CharField(max_length=200)
    ingredient_alternative = models.ForeignKey(IngredientAlternative)
    alternative = models.ManyToManyField(IngredientAlternative, through='AlternativeConsists', related_name='consists')
    recipe = models.ManyToManyField(Recipe, through='Consist')


class AlternativeConsists(models.Model):
    ingredient_alternative = models.ForeignKey(IngredientAlternative)
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.CharField(max_length=200)


class Consist(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.CharField(max_length=200)


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
