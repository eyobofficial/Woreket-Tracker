import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from shared.constants import RETENTION
from shared.models import Product, Customer, Supplier


# Django User
User = get_user_model()

# Rounding decimal
TWO_PLACES = Decimal('0.01')


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
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='created_orders',
        null=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='updated_orders',
        null=True, blank=True
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
        return reverse('orders:open-order-detail', args=[self.pk])

    def touch(self, **kwargs):
        """
        Modifies `updated_at` field to to the current timestamp.
        """
        user = kwargs.get('updated_by')
        if user is not None:
            self.updated_by = user
        self.updated_at = timezone.now()
        self.save()

    def is_fully_allocated(self):
        """Checks if all regions are allocated.

        Returns:
            True (bool): If all regions are allocated
            False (bool): If all regions are not fully allocated yet
        """
        customers = Customer.objects.all()
        allocated_buyers = self.order_allocations.values_list('buyer',
                                                              flat=True)

        for customer in customers:
            if customer.pk not in allocated_buyers:
                return False
        return True

    def get_total_quantity(self):
        """Returns the total quantity in Meteric Ton (MT).

        Returns:
            quantity (Decimal): the total allocated quantity in MT
        """
        quantity = Decimal('0')
        for allocation in self.order_allocations.all():
            quantity += allocation.quantity
        return quantity

    def get_total_amount(self):
        """Returns the total amount in USD.

        Returns:
            amount (Decimal): the total allocated amount in USD
        """
        amount = Decimal('0')
        for allocation in self.order_allocations.all():
            amount += allocation.get_amount()
        return amount

    def get_total_retention(self):
        """Returns the total retention amount in USD.

        Returns:
            amount (Decimal): the total allocated retention amount in USD
        """
        retention = Decimal('0')
        for allocation in self.order_allocations.all():
            retention += allocation.get_retention()
        return retention


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
        default_related_name = 'order_allocations'
        ordering = ('delivery_order', '-quantity', 'buyer__name', )
        unique_together = ('delivery_order', 'buyer')
        verbose_name = 'Delivery Order Allocation'
        verbose_name_plural = 'Delivery Order Allocations'

    def __str__(self):
        return f'{self.buyer.name} - {self.quantity}'

    def get_amount(self):
        """Returns the total amount for this allocation.

        Returns:
            amount (Decimal): Allocation amount in USD
        """
        amount = self.quantity * self.delivery_order.rate
        return amount.quantize(TWO_PLACES)

    def get_retention(self):
        """Returns the 10% retention amount for this allocation.

        Returns:
            retention (Decimal): 10% retention amount in USD
        """
        amount = self.quantity * self.delivery_order.rate * RETENTION
        return amount.quantize(TWO_PLACES)


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
