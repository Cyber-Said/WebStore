import json
from product.models import Product
from .redis_client import get_redis


def _cart_key(user_id: int) -> str:
    return f"cart:user:{user_id}"


def get_cart(user_id: int) -> dict[int, int]:
    r = get_redis()
    raw = r.get(_cart_key(user_id))
    if not raw:
        return {}
    data = json.loads(raw)
    # JSON keys are strings, convert them back to int
    return {int(k): int(v) for k, v in data.items()}


def save_cart(user_id: int, cart: dict[int, int]) -> None:
    r = get_redis()
    r.set(_cart_key(user_id), json.dumps(cart))


def clear_cart(user_id: int) -> None:
    r = get_redis()
    r.delete(_cart_key(user_id))


def add_item(user_id: int, product_id: int, qty: int) -> dict[int, int]:
    if qty <= 0:
        raise ValueError("qty must be > 0")

    # Ensure product exists and is active
    Product.objects.get(id=product_id, is_active=True)

    cart = get_cart(user_id)
    cart[product_id] = cart.get(product_id, 0) + qty
    save_cart(user_id, cart)
    return cart


def set_qty(user_id: int, product_id: int, qty: int) -> dict[int, int]:
    # qty=0 means remove item
    cart = get_cart(user_id)

    if qty <= 0:
        cart.pop(product_id, None)
        save_cart(user_id, cart)
        return cart

    Product.objects.get(id=product_id, is_active=True)
    cart[product_id] = qty
    save_cart(user_id, cart)
    return cart


def remove_item(user_id: int, product_id: int) -> dict[int, int]:
    cart = get_cart(user_id)
    cart.pop(product_id, None)
    save_cart(user_id, cart)
    return cart