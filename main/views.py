import json
from django.shortcuts import render, Http404, redirect
from django.http import JsonResponse

from stripe_task.settings import STRIPE_PUBLISH_KEY
from .utils import *


def get_session(request, id: int):
    item = item_exists(id)
    if not item:
        return JsonResponse({'status': 404, 'msg': f'No item with id: {id}'})
    result, session = create_session(item)
    if not result:
        return JsonResponse({'status': 400, 'message': str(session)})
    return JsonResponse({'id': session.get('id')})


def get_order_session(request, id: int):
    order = order_exists(id)
    if not order:
        return JsonResponse({'status': 404, 'msg': f'No order with id: {id}'})
    result, session = create_order_session(order)
    if not result:
        return JsonResponse({'status': 400, 'message': str(session)})
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
        return JsonResponse({'status': 400, 'message': 'Error payment create'})

    return JsonResponse({'paymentId': payment.get('id')})


def all_items(request):
    context = {
        'items': Item.objects.all(),
        'order_id': Order.objects.get(user=request.user).id,
    }
    return render(request, 'items.html', context)


def item_buy(request, id: int):
    item = item_exists(id)
    if not item:
        raise Http404(f"Not found item with id: {id}")
    context = {
        'item': item,
        'PUBLISH_KEY': STRIPE_PUBLISH_KEY
    }
    if request.method == 'GET':
        return render(request, 'item.html', context)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        count = request.POST.get('count')
        try:
            count = int(count)
        except:
            return JsonResponse({'status': 400, 'error': 'Incorrect count value'})
        if count <= 0:
            return JsonResponse({'status': 400, 'error': 'Incorrect count value'})
        if item.quantity == 0:
            return JsonResponse({'status': 400, 'error': 'Items are over.'})
        if count > item.quantity:
            return JsonResponse({'status': 400, 'error': f'Not enough items. Left: {item.quantity}'})
        if user_id and id:
            res = edit_order(user_id, item, count)
            if res:
                return JsonResponse({'status': 200})
    return JsonResponse({'status': 400, 'error': 'Incorrect item or user_id'})


def order_buy(request, id: int):
    order = order_exists(id)
    if not order:
        raise Http404(f"Not found order with id: {id}")
    context = {
        'order': order,
        'PUBLISH_KEY': STRIPE_PUBLISH_KEY
    }
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id:
            return JsonResponse({'status': 400, 'error': 'Incorrect item_id value.'})
        item = Item.objects.filter(id=item_id).first()
        if not item:
            return JsonResponse({'status': 400, 'error': 'Incorrect item_id value.'})
        order_item = order.items.filter(item=item).first()
        if not order_item:
            return JsonResponse({'status': 400, 'error': 'Incorrect item_id value.'})
        item.quantity += order_item.quantity
        item.save()
        order_item.delete()
        return JsonResponse({'status': 200})
    return render(request, 'order.html', context)
