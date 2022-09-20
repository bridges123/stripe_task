from django.urls import path

from .views import *

urlpatterns = [
    path('buy/<int:id>', get_session, name='get_session'),
    path('order-buy/<int:id>', get_order_session, name='get_order_session'),
    path('item/<int:id>', item_buy, name='item_buy'),
    path('order/<int:id>', order_buy, name='order_buy'),
    path('items/', all_items, name='all_items'),
]
