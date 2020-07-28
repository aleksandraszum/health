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
    date = models.DateField()
    habits1 = models.TextField(max_length=200, null=False)
    habits2 = models.TextField(max_length=200, null=False)
    habits3 = models.TextField(max_length=200, null=False)

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
