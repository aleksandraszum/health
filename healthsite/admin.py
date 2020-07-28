from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.MealPlan)
admin.site.register(models.EatingHabit)
admin.site.register(models.Exercise)

