from django.db import models


class Product(models.Model):
    title = models.CharField('Title', max_length=200)
    image = models.CharField('Image', max_length=200)
    likes = models.PositiveIntegerField(default=0)


class User(models.Model):
    pass
