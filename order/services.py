from django.db import transaction

from cart.services import clear_cart, get_cart
from product.models import Product

from .models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(user_id: int) -> Order:
    cart = get_cart(user_id)  # {product_id: qty}
    if not cart:
        raise ValueError("Cart is empty")

    # Fetch all products in a single query.
    products = Product.objects.filter(id__in=cart.keys(), is_active=True)
    products_map = {p.id: p for p in products}

    # Validate ids that are missing or inactive.
    missing = [pid for pid in cart.keys() if pid not in products_map]
    if missing:
        raise ValueError(f"Some products are missing or inactive: {missing}")

    order = Order.objects.create(user_id=user_id)

    items = []
    for pid, qty in cart.items():
        p = products_map[pid]
        items.append(
            OrderItem(
                order=order,
                product=p,
                unit_price=p.price,
                qty=qty,
            )
        )
    OrderItem.objects.bulk_create(items)

    # Clear cart only after successful order/item persistence.
    clear_cart(user_id)
    return order