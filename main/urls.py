from django.urls import path

from .views import *

urlpatterns = [
    path('buy/<int:id>', get_session, name='get_payment'),
    path('item/<int:id>', item_buy, name='item_buy'),
]
