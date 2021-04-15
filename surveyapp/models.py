from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.category_name)


class Survey(models.Model):
    title_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=100, null=True)
    people = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title_name) + " | " + str(self.category)


class User(AbstractUser):
    points = models.CharField(max_length=200, null=True)


class Questions(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)

    def __str__(self):
        return str(self.question)


class SubmittedSurveys(models.Model):
    user = models.CharField(max_length=50)
    survey = models.CharField(max_length=100)
    questions = models.CharField(max_length=200, default=".")
    answers = models.CharField(max_length=200, default=".")

    def __str__(self):
        return self.survey