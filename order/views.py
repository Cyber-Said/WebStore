from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from .services import create_order_from_cart


class OrdersView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related("items__product")
            .order_by("-id")
        )

        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):

        try:
            order = create_order_from_cart(request.user.id)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = (
            Order.objects
            .prefetch_related("items__product")
            .get(id=order.id)
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class AdminOrdersView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        orders = (
            Order.objects
            .all()
            .prefetch_related("items__product")
            .order_by("-id")
        )

        return Response(OrderSerializer(orders, many=True).data)


class AdminOrderStatusView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):

        order = get_object_or_404(Order, id=order_id)

        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order.status = serializer.validated_data["status"]
        order.save(update_fields=["status", "updated_at"])

        order = (
            Order.objects
            .prefetch_related("items__product")
            .get(id=order.id)
        )

        return Response(OrderSerializer(order).data)
