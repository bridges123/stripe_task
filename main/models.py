from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

CURRENCY_CHOICES = [
    ('rub', '₽'),
    ('usd', '$'),
    ('eur', '€')
]


def discount_validator(discount):
    if not (1 <= discount <= 99):
        raise ValidationError('Скидка должна быть 1-99%')


class Item(models.Model):
    name = models.CharField('Имя', max_length=255)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
    quantity = models.IntegerField('Количество')
    currency = models.CharField('Валюта', choices=CURRENCY_CHOICES, max_length=3)

    def get_viewed_currency(self):
        for CHOICE in CURRENCY_CHOICES:
            if CHOICE[0] == self.currency:
                return CHOICE[1]
        return self.currency

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=32)
    discount = models.IntegerField('Скидка', validators=[discount_validator])
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return self.code


# Tax has to activate stripe account!
class Tax(models.Model):
    name = models.CharField('Название', max_length=255)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return f'Tax №{self.id}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', verbose_name='Пользователь')
    discounts = models.ManyToManyField(Discount, related_name='orders', verbose_name='Скидки')
    taxes = models.ManyToManyField(Tax, related_name='orders', verbose_name='Налоги')

    def add(self, item, quantity=1):
        OrderItem.objects.create(item=item, order=self, quantity=quantity)

    def get_total_price(self):
        return sum([item.item.price * item.quantity for item in self.items.all()])

    total_price = property(get_total_price)

    def __str__(self):
        return f'Order №{self.id}'


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order', verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    quantity = models.IntegerField('Количество')

    def __str__(self):
        return f'{self.item} -> {self.order}'
