import uuid

from django.db import models

from django_countries.fields import CountryField


class Region(models.Model):
    """
    Product buyer regions.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        verbose_name = 'Regional State'
        verbose_name_plural = 'Regional States'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    City, town or special location within the region.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    name = models.CharField(max_length=120)

    class Meta:
        order_with_respect_to = 'region'

    def __str__(self):
        return self.name


class Union(models.Model):
    """
    Peasant unions.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='unions'
    )
    name = models.CharField(max_length=120)

    class Meta:
        order_with_respect_to = 'region'

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


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    company_name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    country = CountryField()

    class Meta:
        ordering = ('company_name', )

    def __str__(self):
        return self.company_name
