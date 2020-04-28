import datetime
import uuid

from django.db import models
from django_countries.fields import CountryField

from shared.models import Unit


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
    current_year = datetime.date.today().year
    YEAR_CHOICES = [(y, y) for y in range(current_year - 2, current_year + 4)]

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
    batch_round = models.PositiveSmallIntegerField(
        default=1,
        help_text='Batch round for the year.'
    )
    year = models.PositiveIntegerField(
        choices=YEAR_CHOICES,
        default=current_year
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name='batches'
        verbose_name = 'Purchasing Batch'
        verbose_name_plural = 'Purchasing Batches'
        unique_together = ('name', 'product', 'batch_round', 'year')
        ordering = ('-created_at', )

    def __str__(self):
        return '{name}/Product: {product}/Year: {year}({batch_round})'.format(
            name=self.name,
            product=self.product.name,
            year=self.year,
            batch_round=self.batch_round
        )
