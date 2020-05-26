# Generated by Django 2.2.11 on 2020-05-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0005_auto_20200513_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='quantity',
            field=models.DecimalField(decimal_places=4, help_text='Quantity in the selected product unit.', max_digits=20),
        ),
        migrations.AlterField(
            model_name='batch',
            name='rate',
            field=models.DecimalField(decimal_places=4, help_text='Price is in USD.', max_digits=12),
        ),
    ]