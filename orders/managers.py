from django.db import models


class BatchManager(models.Manager):
    """Custom ORM manager for the Batch model."""

    def get_queryset(self, *args, **kwargs):
        """Returns a queryset by removing deleted batches."""
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_deleted=False)
        return qs
