# Generated by Django 2.2.11 on 2020-06-13 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20200609_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryorder',
            name='quantity',
        ),
    ]