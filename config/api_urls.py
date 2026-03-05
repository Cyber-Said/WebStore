from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from cart.views import CartAddItemView, CartItemView, CartView
from order.views import AdminOrdersView, AdminOrderStatusView, OrdersView
from product.views import ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]

urlpatterns += [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/items/", CartAddItemView.as_view(), name="cart_add_item"),
    path("cart/items/<int:product_id>/", CartItemView.as_view(), name="cart_item"),
]

urlpatterns += [
    path("orders/", OrdersView.as_view(), name="orders"),
    path("admin/orders/", AdminOrdersView.as_view(), name="admin_orders"),
    path(
        "admin/orders/<int:order_id>/status/",
        AdminOrderStatusView.as_view(),
        name="admin_order_status",
    ),
]
