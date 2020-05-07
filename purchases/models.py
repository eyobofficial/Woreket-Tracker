import pendulum
import uuid

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

from shared.models import Unit
from orders.models import DeliveryOrder

from .managers import BatchManager


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField('company name', max_length=60)
    city = models.CharField(max_length=60)
    country = CountryField()

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    """
    Category of products available for purchase.
    """
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name', )
        default_related_name = 'products'

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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=120)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Quantity in the selected product unit.'
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price is in USD.'
    )
    year = models.PositiveIntegerField(
        choices=YEAR_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField('deleted', default=False)

    # Custom manager
    objects = BatchManager()

    class Meta:
        default_related_name='batches'
        verbose_name = 'Purchasing Batch'
        verbose_name_plural = 'Purchasing Batches'
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.name} ({self.product}) - {self.get_year_display()}'

    def get_amount(self):
        """Returns the total amount for the batch."""
        return round(self.quantity * self.rate, 2)
