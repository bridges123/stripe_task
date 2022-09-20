from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField('Имя', max_length=255)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
    quantity = models.IntegerField('Количество')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', verbose_name='Пользователь')

    def add(self, item, quantity=1):
        OrderItem.objects.create(item=item, order=self, quantity=quantity)

    def get_total_price(self):
        return sum([item.item.price * item.quantity for item in self.items.all()])

    total_price = property(get_total_price)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order', verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    quantity = models.IntegerField('Количество')
