import uuid

from django.db import models

from django_countries.fields import CountryField


class Customer(models.Model):
    """
    Customer that is paying for the product.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        max_length=120,
        help_text='Customer company or office name.'
    )
    region = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    City, town or special location within the cutomer's region
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    name = models.CharField(max_length=120)

    class Meta:
        order_with_respect_to = 'customer'

    def __str__(self):
        return self.name


class Union(models.Model):
    """
    Regional unions.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='unions'
    )
    name = models.CharField(max_length=120)

    class Meta:
        order_with_respect_to = 'customer'

    def __str__(self):
        return self.name



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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products'
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name
