import uuid

from django.db import models
from django.urls import reverse

from shared.models import Product, Region


class CreditLetter(models.Model):
    """
    Letter of credit for fertilizer and bag payments.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    document_number = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='credit_letters'
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price is in USD.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Letter of Credit'
        verbose_name_plural = 'Letter of Credits'
        ordering = ('-created_at', )

    def __str__(self):
        return self.document_number

    def get_absolute_url(self):
        return reverse('retentions:lc-detail', args=[self.pk])


class DeliveryOrder(models.Model):
    """
    LC delivery order for regions.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    lc = models.ForeignKey(
        CreditLetter,
        on_delete=models.SET_NULL, null=True,
        verbose_name='letter of credit'
    )
    buyer = models.ForeignKey(
        Region,
        null=True,
        on_delete=models.SET_NULL
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='In meteric ton (MT)'
    )

    class Meta:
        default_related_name = 'delivery_orders'
        ordering = ('buyer__name', )
        unique_together = ('lc', 'buyer')
        verbose_name = 'Delivery Order'
        verbose_name_plural = 'Delivery Orders'

    def __str__(self):
        return f'{self.buyer.name} - {self.quantity}'


class InspectionReport(models.Model):
    """
    Inspection report for retention.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    retention = models.OneToOneField(
        CreditLetter,
        on_delete=models.CASCADE,
        related_name='inspection_report'
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='In meteric ton (MT)'
    )

    def __str__(self):
        return self.retention
