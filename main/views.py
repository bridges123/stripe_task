import stripe
from django.shortcuts import render, Http404, reverse
from django.http import JsonResponse

from .models import Item


def get_session(request, id: int):
    item = Item.objects.filter(id=id).first()
    if not item:
        return JsonResponse({'status': 404, 'msg': f'No item with id: {id}'})
    try:
        payment = stripe.PaymentIntent.create(
            amount=item.price,
            currency='usd',
            payment_method='pm_card_visa'
        )
    except Exception as ex:
        print(ex)
        return JsonResponse({'status': 500, 'message': 'Error payment create'})

    return JsonResponse({'paymentId': payment.get('id')})
