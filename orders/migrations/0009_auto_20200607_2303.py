# Generated by Django 2.2.11 on 2020-06-07 20:03
from django.db import migrations

def move_batch_model(apps, schema_editor):
    """
    Moves the `Batch` model from the `purchases` app to the
    `orders` app.
    """
    OldBatch = apps.get_model('purchases', 'Batch')
    NewBatch = apps.get_model('orders', 'Batch')
    batches = OldBatch.objects.all()
    for batch in batches:
        kwargs = dict(
            id=batch.pk, name=batch.name, lc_number=batch.lc_number,
            product=batch.product, supplier=batch.supplier,
            quantity=batch.quantity, rate=batch.rate, year=batch.year,
            status=batch.status, is_deleted=batch.is_deleted,
            created_at=batch.created_at, updated_at=batch.update_at
        )
        NewBatch.objects.create(**kwargs)


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_batch'),
        ('purchases', '0010_auto_20200606_1609')
    ]

    operations = [
        migrations.RunPython(move_batch_model),
    ]
