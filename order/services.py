from django.db import transaction

from product.models import Product
from cart.services import get_cart, clear_cart

from .models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(user_id: int) -> Order:

    cart = get_cart(user_id)

    if not cart:
        raise ValueError("Cart is empty")

    products = Product.objects.filter(
        id__in=cart.keys(),
        is_active=True
    )

    products_map = {p.id: p for p in products}

    missing = [pid for pid in cart.keys() if pid not in products_map]

    if missing:
        raise ValueError(f"Products unavailable: {missing}")

    order = Order.objects.create(user_id=user_id)

    items = []

    for product_id, qty in cart.items():

        product = products_map[product_id]

        items.append(
            OrderItem(
                order=order,
                product=product,
                unit_price=product.price,
                qty=qty
            )
        )

    OrderItem.objects.bulk_create(items)

    clear_cart(user_id)

    return order
