import stripe

from .models import Item, Order


def item_exists(id: int):
    item = Item.objects.filter(id=id).first()
    return item


def order_exists(id: int):
    order = Order.objects.filter(id=id).first()
    return order


def create_session(items: list):
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
