# Generated by Django 2.2.11 on 2020-06-06 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_deliveryorder_lc_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryorder',
            name='status',
        ),
    ]