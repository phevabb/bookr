from django.db import models


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=222)
    author = models.CharField(max_length=56)
