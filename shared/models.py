import uuid

from django.db import models


class Unit(models.Model):
    """Measurement units."""
    WEIGHT = 'WEIGHT'
    VOLUME = 'VOLUME'
    LENGTH = 'LENGTH'
    COUNTER = 'COUNTER'

    TYPE_CHOICES = (
        (WEIGHT, 'Weight/Mass'),
        (VOLUME, 'Volume'),
        (LENGTH, 'Length/Distance'),
        (COUNTER, 'Counter')
    )

    name = models.CharField(max_length=60)
    code = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'

    def __str__(self):
        return self.name
