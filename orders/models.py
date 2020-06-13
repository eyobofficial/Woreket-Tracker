import uuid
import pendulum
from decimal import Decimal
from functools import reduce

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from django_countries import Countries
from django_countries.fields import CountryField

from shared.constants import ADVANCE, RETENTION
from shared.models import Unit
from customers.models import Customer, Union, Location


User = settings.AUTH_USER_MODEL


class NeighbourCountry(Countries):
    only = ['DJ', 'ER', 'SO', 'SD', 'KE']


class Port(models.Model):
    """Dispatch ports."""
    name = models.CharField(max_length=120, unique=True)
    country = CountryField(countries=NeighbourCountry)
    office = models.CharField(max_length=120, blank=True)
    is_default = models.BooleanField('default', default=False)

    class Meta:
        ordering = ('-is_default', 'name')
        verbose_name = 'Dispatch Port'
        verbose_name_plural = 'Dispatch Ports'

    def __str__(self):
        return self.name


class Batch(models.Model):
    """Product purchasing batches."""
    today = pendulum.today(tz=settings.TIME_ZONE)
    choice_duration = 5
    ethiopian_year = today.year - 7

    YEAR_CHOICES = [
        (y, f'{y}/{y + 1}')
        for y in range(ethiopian_year - choice_duration, ethiopian_year)
    ]

    # Status
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = (
        (OPEN, 'open'),
        (CLOSED, 'closed')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=120)
    lc_number = models.CharField(
        'L/C number', max_length=30,
        help_text='Document number for the letter of credit.'
    )
    product = models.ForeignKey(
        'purchases.Product',
        null=True, on_delete=models.SET_NULL
    )
    supplier = models.ForeignKey(
        'purchases.Supplier',
        null=True, on_delete=models.SET_NULL
    )
    quantity = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        help_text='Quantity in the selected product unit.'
    )
    rate = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        help_text='Price is in USD.'
    )
    year = models.PositiveIntegerField(
        choices=YEAR_CHOICES,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name='batches'
        verbose_name = 'Purchasing Batch'
        verbose_name_plural = 'Purchasing Batches'
        ordering = ('-created_at', )
        permissions = [
            ('close_batch', 'Close purchasing batch'),
            ('reopen_batch', 'Re-open purchasing batch')
        ]

    def __str__(self):
        return f'{self.name} ({self.product}) - {self.get_year_display()}'

    def get_absolute_url(self):
        return reverse('orders:batch-detail', args=[self.pk])

    def get_agreement_amount(self):
        """Returns the amount as per the agreement in USD.

        Returns:
            amount (Decimal): total agreement amount in USD
        """
        return round(self.quantity * self.rate, 4)

    def get_allocated_quantity(self):
        """Returns the total allocated (actual) quantity.

        Return:
            quantity (Decimal): total allocated quantity in product unit
        """
        delivery_orders = self.delivery_orders.all()
        quantity = reduce(
            lambda total, order: total + order.get_allocated_quantity(),
            delivery_orders,
            Decimal(0)
        )
        return quantity

    def get_allocated_amount(self):
        """Returns the total allocated (actual) amount.

        Return:
            amount (Decimal): total allocated amount in USD.
        """
        delivery_orders = self.delivery_orders.all()
        amount = reduce(
            lambda total, order: total + order.get_allocated_amount(),
            delivery_orders,
            Decimal(0)
        )
        return amount

    def get_advance_amount(self):
        """Returns the 90% allocated advance amount.

        Return:
            amount (Decimal): total 90% allocated advance amount in USD.
        """
        delivery_orders = self.delivery_orders.all()
        amount = reduce(
            lambda total, order: total + order.get_allocated_advance(),
            delivery_orders,
            Decimal(0)
        )
        return amount

    def get_retention_amount(self):
        """Returns the 10% allocated retention amount.

        Return:
            amount (Decimal): total 10% allocated retention amount in USD.
        """
        delivery_orders = self.delivery_orders.all()
        amount = reduce(
            lambda total, order: total + order.get_allocated_retention(),
            delivery_orders,
            Decimal(0)
        )
        return amount

    def get_distributed_quantity(self):
        """Returns the total distributed (actual) quantity.

        Return:
            quantity (Decimal): total distributed quantity in product unit
        """
        delivery_orders = self.delivery_orders.all()
        quantity = reduce(
            lambda total, order: total + order.get_distributed_quantity(),
            delivery_orders,
            Decimal(0)
        )
        return quantity

    def get_distributed_shortage(self):
        """Returns the total distributed shortage (actual) quantity.

        Return:
            quantity (Decimal): total distributed shortage in product unit
        """
        delivery_orders = self.delivery_orders.all()
        quantity = reduce(
            lambda total, order: total + order.get_distributed_shortage(),
            delivery_orders,
            Decimal(0)
        )
        return quantity

    def get_distributed_amount(self):
        """Returns the total distributed (actual) amount.

        Return:
            amount (Decimal): total distributed amount in USD.
        """
        delivery_orders = self.delivery_orders.all()
        amount = reduce(
            lambda total, order: total + order.get_distributed_amount(),
            delivery_orders,
            Decimal(0)
        )
        return amount


class DeliveryOrder(models.Model):
    """Product delivery orders."""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    vessel = models.CharField(max_length=120, help_text='Shipment vessel name.')
    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    bill_of_loading = models.CharField(
        max_length=30,
        help_text='Bill of loading (B/L) number.'
    )
    port = models.ForeignKey(
        Port,
        null=True,
        on_delete=models.SET_NULL,
    )
    arrival_date = models.DateField('vessel arrival date')
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
        ordering = ('created_at', )
        permissions = [
            ('close_deliveryorder', 'Close delivery order'),
            ('reopen_deliveryorder', 'Re-open delivery order')
        ]
        verbose_name = 'Delivery Order'
        verbose_name_plural = 'Delivery Orders'

    def __str__(self):
        return self.vessel

    @property
    def unit(self):
        return self.batch.product.unit

    @property
    def lc_number(self):
        return self.batch.lc_number

    @property
    def status(self):
        return self.batch.status

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
        allocated_buyers = self.allocations.values_list('buyer', flat=True)

        for customer in customers:
            if customer.pk not in allocated_buyers:
                return False
        return True

    def is_fully_distributed(self):
        """Checks if distribution data is added to all allocated regions.

        Returns:
            True (bool): If all allocated regions have distribtion data
            False (bool): If some allocated regions are missing distribution
                          data
        """
        customers = Customer.objects.all()
        distributed_buyers = self.distributions.values_list('buyer', flat=True)

        for customer in customers:
            if customer.pk not in distributed_buyers:
                return False
        return True

    def get_allocated_quantity(self):
        """Returns the total allocated quantity in product unit.

        Returns:
            quantity (Decimal): the total allocated quantity
        """
        quantity = Decimal('0')
        for allocation in self.allocations.all():
            quantity += allocation.get_total_quantity()
        return round(quantity, 4)

    def get_distributed_quantity(self):
        """Returns the total distributed quantity in product unit.

        Returns:
            quantity (Decimal): the total distributed quantity
        """
        quantity = Decimal('0')
        for distribution in self.distributions.all():
            quantity += distribution.get_total_quantity()
        return round(quantity, 4)

    def get_distributed_shortage(self):
        """Returns the difference between the total allocated quantity
           and the actual delivered quantity.

        Returns:
            quantity (Decimal): quantity shortage between allocated & delivered
        """
        quantity = Decimal('0')
        for distribution in self.distributions.all():
            quantity += distribution.get_total_shortage()
        return round(quantity, 4)

    def get_allocated_amount(self):
        """Returns the total allocated amount in USD.

        Returns:
            amount (Decimal): the total allocated amount in USD
        """
        amount = Decimal('0')
        for allocation in self.allocations.all():
            amount += allocation.get_amount()
        return round(amount, 4)

    def get_allocated_advance(self):
        """Returns the total allocated advance amount in USD.

        Returns:
            amount (Decimal): the total allocated advance amount in USD
        """
        return round(self.get_allocated_amount() * ADVANCE)

    def get_allocated_retention(self):
        """Returns the total allocated retention amount in USD.

        Returns:
            amount (Decimal): the total allocated retention amount in USD
        """
        return round(self.get_allocated_amount() * RETENTION)

    def get_distributed_amount(self):
        """Returns the total delivered amount in USD.

        Returns:
            amount (Decimal): the total delivered amount in USD
        """
        amount = Decimal('0')
        for distribution in self.distributions.all():
            amount += distribution.get_amount()
        return round(amount, 4)


class Allocation(models.Model):
    """Region allocation for delivery orders."""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    delivery_order = models.ForeignKey(DeliveryOrder,on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='created_allocations',
        null=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='updated_allocations',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'allocations'
        ordering = ('delivery_order', 'created_at', )
        unique_together = ('delivery_order', 'buyer')
        verbose_name = 'Delivery Order Allocation'
        verbose_name_plural = 'Delivery Order Allocations'

    def __str__(self):
        return f'{self.buyer.name} - {self.get_total_quantity()}'

    def get_total_quantity(self):
        """Returns the total allocation quantity.

        Returns:
            quantity (Decimal): total allocated quantities of the unions
        """
        union_allocations = self.union_allocations.all()
        quantity = reduce(
            lambda total, union: total + union.quantity,
            union_allocations,
            Decimal(0)
        )
        return round(quantity, 4)

    def get_amount(self):
        """Returns the total amount for this allocation.

        Returns:
            amount (Decimal): Allocation amount in USD
        """
        amount = self.get_total_quantity() * self.delivery_order.batch.rate
        return round(amount, 4)

    def get_percentage(self):
        """Returns the region allocation percentage.

        Returns:
            percentage (Decimal): allocation quantity in percent.
        """
        quantity = self.get_total_quantity()
        total_allocation = self.delivery_order.get_allocated_quantity()
        percent = (quantity / total_allocation) * 100
        return round(percent, 2)

class UnionAllocation(models.Model):
    """Allocation data to the unions for the delivery order."""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE)
    union = models.ForeignKey(Union, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        'allocated quantity',
        max_digits=20, decimal_places=4,
        help_text='Quantity allocated to the union in product unit.'
    )

    class Meta:
        order_with_respect_to = 'allocation'
        default_related_name  = 'union_allocations'

    def __str__(self):
        return f'{self.union.name} allocation'


class Distribution(models.Model):
    """Actual distribution data for the delivery order."""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    delivery_order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='created_distributions',
        null=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='updated_distributions',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'distributions'
        ordering = ('delivery_order', 'created_at')
        unique_together = ('delivery_order', 'buyer')
        verbose_name = 'Delivery Order Distribution'
        verbose_name_plural = 'Delivery Order Distributions'

    def __str__(self):
        return f'{self.delivery_order} distribution'

    def get_allocation(self):
        """Returns the respective allocation for this distribution.

        Returns:
            quantity (Decimal): allocated quantity if it exists
            None: if no quantity is allocated for this distribution
        """
        try:
            allocation = Allocation.objects.get(
                delivery_order=self.delivery_order,
                buyer=self.buyer
            )
            return allocation.quantity
        except Allocation.DoesNotExist:
            return

    def get_total_quantity(self):
        """Returns the distribution quantity with shortage and over supply.

        Returns:
            quantity (Decimal): received quantity + shortage + over
        """
        union_distributions = self.union_distributions.all()
        quantity = reduce(
            lambda total, union: total + union.get_total_quantity(),
            union_distributions,
            Decimal(0)
        )
        return round(quantity, 4)

    def get_total_shortage(self):
        """Returns the distribution shortage quantity.

        Returns:
            shortage quantity (Decimal): received shortage + over
        """
        union_distributions = self.union_distributions.all()
        quantity = reduce(
            lambda total, union: total + union.get_total_shortage(),
            union_distributions,
            Decimal(0)
        )
        return round(quantity, 4)

    def get_amount(self):
        """Returns the total amount for this distribution.

        Returns:
            amount (Decimal): Distribution amount in USD
        """
        amount = self.get_total_quantity() * self.delivery_order.batch.rate
        return round(amount, 4)

    def get_retention(self):
        """Returns the 10% retention amount for this dis.

        Returns:
            retention (Decimal): 10% retention amount in USD
        """
        rate = self.delivery_order.batch.rate
        amount = self.get_total_quantity() * rate * RETENTION
        return round(amount, 4)

    def get_percentage(self):
        """Returns the region distribution percentage.

        Returns:
            percentage (Decimal): distribution quantity in percent.
        """
        quantity = self.get_total_quantity()
        total_distribution = self.delivery_order.get_distributed_quantity()
        percent = (quantity / total_distribution) * 100
        return round(percent, 2)


class UnionDistribution(models.Model):
    """Actual distribution data to the unions for the delivery order."""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    union = models.ForeignKey(Union, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        'received quantity',
        max_digits=16, decimal_places=4,
        help_text='Quantity received by the union in product unit.'
    )
    shortage = models.DecimalField(
        'dispatch shortage',
        max_digits=20, decimal_places=4,
        help_text='Quantity deficit after transportation in product unit.'
    )
    over = models.DecimalField(
        'over supplied quantity',
        max_digits=20, decimal_places=4,
        help_text='Over quantity supplied in product unit.'
    )

    class Meta:
        order_with_respect_to = 'distribution'
        default_related_name  = 'union_distributions'

    def __str__(self):
        return f'{self.union.name} distribution'

    def get_total_quantity(self):
        """Returns the distribution quantity with shortage and over supply.

        Returns:
            quantity (Decimal): received quantity + shortage + over
        """
        return round(self.quantity + self.shortage + self.over, 4)

    def get_total_shortage(self):
        """Returns the distribution total shortage.

        Returns:
            shortage quantity (Decimal): received shortage + over
        """
        return round(self.shortage + self.over, 4)
