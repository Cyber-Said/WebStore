from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from .serializers import CartAddSerializer, CartSetQtySerializer
from .services import add_item, get_cart, remove_item, set_qty


def _cart_response(user_id: int):
    cart = get_cart(user_id)  # {product_id: qty}
    product_ids = list(cart.keys())

    products = Product.objects.filter(id__in=product_ids)
    products_map = {p.id: p for p in products}

    items = []
    total = 0

    for pid, qty in cart.items():
        p = products_map.get(pid)
        if not p:
            continue
        line_total = float(p.price) * qty
        total += line_total
        items.append(
            {
                "product_id": pid,
                "name": p.name,
                "price": str(p.price),
                "qty": qty,
                "line_total": round(line_total, 2),
            }
        )

    return {"items": items, "total": round(total, 2)}


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(_cart_response(request.user.id))


class CartAddItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = CartAddSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        add_item(
            user_id=request.user.id,
            product_id=s.validated_data["product_id"],
            qty=s.validated_data["qty"],
        )
        return Response(_cart_response(request.user.id))


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id: int):
        s = CartSetQtySerializer(data=request.data)
        s.is_valid(raise_exception=True)
        set_qty(
            user_id=request.user.id,
            product_id=product_id,
            qty=s.validated_data["qty"],
        )
        return Response(_cart_response(request.user.id))

    def delete(self, request, product_id: int):
        remove_item(user_id=request.user.id, product_id=product_id)
        return Response(_cart_response(request.user.id))
