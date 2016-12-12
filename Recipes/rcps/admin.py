from django.contrib import admin

# Register your models here.
from rcps.models import *


class IngredientToRecipeInline(admin.TabularInline):
    model = Ingredient.recipes.through
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class EquipmentInline(admin.TabularInline):
    model = Equipment.equipment_recipes.through
    verbose_name = 'Инструмент'
    verbose_name_plural = 'Инструменты'


class TagInline(admin.TabularInline):
    model = Tag.tag_recipes.through
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    fields = ['recipe_name', 'recipe_link']
    inlines = (
        IngredientToRecipeInline,
        EquipmentInline,
        TagInline,
    )


class IngredientComponentInAlternativeInline(admin.TabularInline):
    model = IngredientAlternative.ingredients.through
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class IngredientAlternativeAdmin(admin.ModelAdmin):
    model = IngredientAlternative
    inlines = (
        IngredientComponentInAlternativeInline,
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientAlternative, IngredientAlternativeAdmin)
admin.site.register(IngredientCategory)
admin.site.register(Equipment)
admin.site.register(EquipmentCategory)
admin.site.register(IngredientReplacement)
admin.site.register(Tag)