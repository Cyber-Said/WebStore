from django.conf import settings
from django.db import models
from django.utils import timezone

from product.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.CREATED,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    # Keep price snapshot at order time.
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    qty = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.qty}"
