import stripe

from .models import Item, Order


def item_exists(id: int) -> Item | None:
    item = Item.objects.filter(id=id).first()
    return item


def order_exists(id: int) -> Order | None:
    order = Order.objects.filter(id=id).first()
    return order


def edit_order(user_id: int, item: Item, count: int) -> bool:
    order = Order.objects.filter(user_id=user_id).first()
    if order and item:
        if order.items.all().filter(item_id=item.id).first():
            cur_order = order.items.get(item_id=item.id)
            cur_order.quantity += count
            cur_order.save()
        else:
            order.add(item, count)
        item.quantity -= count
        item.save()
        return True
    return False


def create_session(item: Item) -> tuple:
    try:
        session = stripe.checkout.Session.create(
            success_url="https://127.0.0.1/",
            cancel_url="https://127.0.0.1/",
            line_items=[
                {
                    "price_data": {
                        "unit_amount": item.price * 100,
                        "currency": "usd",
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
        )
        return True, session
    except Exception as ex:
        return False, ex


def create_order_session(items: list) -> tuple:
    try:
        session = stripe.checkout.Session.create(
            success_url="https://127.0.0.1/",
            cancel_url="https://127.0.0.1/",
            line_items=[
                {
                    "price_data": {
                        "unit_amount": item.item.price * 100,
                        "currency": "usd",
                        'product_data': {
                            'name': item.item.name,
                            'description': item.item.description,
                        },
                    },
                    "quantity": 1,
                } for item in items
            ],
            mode="payment",
        )
        return True, session
    except Exception as ex:
        return False, ex


def create_payment(item: Item):
    try:
        session = stripe.checkout.Session.create(
            success_url="https://127.0.0.1/",
            cancel_url="https://127.0.0.1/",
            line_items=[
                {
                    "price_data": {
                        "unit_amount": item.price,
                        "currency": "usd",
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        return session
    except Exception as ex:
        return ex
