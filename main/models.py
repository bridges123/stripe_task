from django.db import models


class Item(models.Model):
    name = models.CharField('Имя', max_length=255)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
