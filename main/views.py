from django.shortcuts import render, Http404, reverse
from django.http import JsonResponse

from .utils import item_exists, create_session, create_payment


def get_session(request, id: int):
    item = item_exists(id)
    if not item:
        return JsonResponse({'status': 404, 'msg': f'No item with id: {id}'})
    result, session = create_session(item)
    if not result:
        return JsonResponse({'status': 500, 'message': str(session)})
    return JsonResponse({'id': session.get('id')})


def get_payment(request, id: int):
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


def item_buy(request, id: int):
    item = item_exists(id)
    if not item:
        raise Http404(f"Not found item with id: {id}")
    context = {
        'item': item
    }
    return render(request, 'index.html', context)
