import pendulum
import uuid

from decimal import Decimal
from functools import reduce

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

from phonenumber_field.modelfields import PhoneNumberField

from shared.constants import ADVANCE, RETENTION
from shared.models import Unit
# from orders.models import DeliveryOrder

from .managers import BatchManager


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField('company name', max_length=60)
    short_name = models.CharField('abbreviation', max_length=60, blank=True)
    email = models.EmailField(max_length=60, blank=True)
    phone_number = PhoneNumberField(null=True, unique=True)
    fax_number = PhoneNumberField(null=True, unique=True)
    city = models.CharField(max_length=60)
    country = CountryField()

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.short_name or self.name


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
