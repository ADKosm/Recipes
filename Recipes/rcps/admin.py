from django.contrib import admin

# Register your models here.
from rcps.models import *


class RecipeAdmin(admin.ModelAdmin):
    fields = ['recipe_name', 'recipe_link']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientAlternative)
admin.site.register(IngredientCategory)
