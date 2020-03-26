import uuid

from django.db import models
from django.urls import reverse

from shared.models import Product, Customer, Supplier


class DeliveryOrder(models.Model):
    """Product delivery orders."""

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = (
        (OPEN, 'open'),
        (CLOSED, 'closed')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    lc_number = models.CharField(
        'letter of credit number',
        max_length=30, unique=True
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price is in USD.'
    )
    vessel = models.CharField(max_length=120, help_text='Shipment vessel name.')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'delivery_orders'
        ordering = ('-created_at', )
        verbose_name = 'Delivery Order'
        verbose_name_plural = 'Delivery Orders'

    def __str__(self):
        return self.lc_number

    def get_absolute_url(self):
        return reverse('orders:delivery-order-detail', args=[self.pk])


class OrderAllocation(models.Model):
    """
    Region allocation for delivery orders
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    delivery_order = models.ForeignKey(DeliveryOrder,on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='In meteric ton (MT)'
    )

    class Meta:
        default_related_name = 'order_allcations'
        ordering = ('buyer__name', )
        unique_together = ('delivery_order', 'buyer')
        verbose_name = 'Delivery Order Allocation'
        verbose_name_plural = 'Delivery Order Allocations'

    def __str__(self):
        return f'{self.buyer.name} - {self.quantity}'


class InspectionReport(models.Model):
    """
    Inspection report for retention.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    delivery_order = models.OneToOneField(
        DeliveryOrder,
        on_delete=models.CASCADE,
        related_name='inspection_report'
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='In meteric ton (MT)'
    )

    def __str__(self):
        return self.delivery_order
