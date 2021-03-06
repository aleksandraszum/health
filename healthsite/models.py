from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    breakfast = models.TextField(null=False, max_length=100)
    lunch = models.TextField(null=False, max_length=100, )
    dinner = models.TextField(null=False, max_length=100)
    supper = models.TextField(null=False, max_length=100)

    def __str__(self):
        return f"{self.user} -{self.date}"

    class Meta:
        unique_together = [['user', 'date']]


class EatingHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    habits1 = models.TextField(max_length=200, null=False)
    habits2 = models.TextField(max_length=200, null=False)
    habits3 = models.TextField(max_length=200, null=False)
    day1 = models.BooleanField(null=True, blank=False)
    day2 = models.BooleanField(null=True, blank=False)
    day3 = models.BooleanField(null=True, blank=False)
    day4 = models.BooleanField(null=True, blank=False)
    day5 = models.BooleanField(null=True, blank=False)
    day6 = models.BooleanField(null=True, blank=False)
    day7 = models.BooleanField(null=True, blank=False)
    day8 = models.BooleanField(null=True, blank=False)
    day9 = models.BooleanField(null=True, blank=False)
    day10 = models.BooleanField(null=True, blank=False)
    day11 = models.BooleanField(null=True, blank=False)
    day12 = models.BooleanField(null=True, blank=False)
    day13 = models.BooleanField(null=True, blank=False)
    day14 = models.BooleanField(null=True, blank=False)
    day15 = models.BooleanField(null=True, blank=False)
    day16 = models.BooleanField(null=True, blank=False)
    day17 = models.BooleanField(null=True, blank=False)
    day18 = models.BooleanField(null=True, blank=False)
    day19 = models.BooleanField(null=True, blank=False)
    day20 = models.BooleanField(null=True, blank=False)
    day21 = models.BooleanField(null=True, blank=False)

    def __str__(self):
        return f"{self.user} -{self.date}"

    class Meta:
        unique_together = [['user', 'date']]


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercise = models.TextField(max_length=200, null=True, blank=True)
    movie = EmbedVideoField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} -{self.date}"

    class Meta:
        unique_together = [['user', 'date']]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    actual_weight = models.FloatField(null=True, blank=True)
    dream_weight = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}"


class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    weight = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.date}"
