import uuid

from django.db import models


class Customer(models.Model):
    """
    Customer that is paying for the product.
    """
    name = models.CharField(
        max_length=120,
        help_text='Customer company or office name.'
    )
    region = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=4, unique=True)

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
