import uuid

from django.db import models


class Region(models.Model):
    """
    Regional states.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=3, unique=True)
    amharic_name = models.CharField(max_length=255)

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
    amharic_name = models.CharField(max_length=255)

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
    amharic_name = models.CharField(max_length=255)

    class Meta:
        order_with_respect_to = 'region'

    def __str__(self):
        return self.name
