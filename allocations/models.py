import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from shared.models import Region, Location, Union


User = get_user_model()


class LC(models.Model):
    """
    Letter of credit.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    document_number = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'Letter of Credit'
        verbose_name_plural = 'Letter of Credits'

    def __str__(self):
        return self.document_number


class Fertilizer(models.Model):
    """
    Fertilizer types.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class DistributionOrder(models.Model):
    """
    Fertilizer distribution order as opened by the purchasing department.
    """
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    status_choices  = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    vessel = models.CharField(
        max_length=120,
        help_text='The name of the transportation vessel.'
    )
    lc = models.ForeignKey(
        LC,
        verbose_name='letter of credit',
        on_delete=models.PROTECT
    )
    fertilizer = models.ForeignKey(
        Fertilizer,
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default=OPEN
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_deleted = models.BooleanField('deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        default_related_name = 'distribution_orders'
        verbose_name = 'Distribution Order'
        verbose_name_plural = 'Distribution Orders'

    def __str__(self):
        return self.vessel

    def get_absolute_url(self):
        return reverse('allocations:distribution-detail', args=[self.pk])

    def get_total_amount(self):
        return


class Allocation(models.Model):
    """
    An allocation item of the distribution order.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    distribution_order = models.ForeignKey(
        DistributionOrder,
        on_delete=models.CASCADE
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    union = models.ForeignKey(Union, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Quantity in meteric ton.'
    )
    is_deleted = models.BooleanField('deleted', default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'distribution_order'
        default_related_name = 'allocations'

    def __str__(self):
        return f'{self.distribution_order} - {self.union}'
