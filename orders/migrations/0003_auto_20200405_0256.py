# Generated by Django 2.2.11 on 2020-04-04 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0001_initial'),
        ('orders', '0002_auto_20200405_0240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdistribution',
            name='order_allocation',
        ),
        migrations.RemoveField(
            model_name='orderdistribution',
            name='received_quantity',
        ),
        migrations.AddField(
            model_name='orderdistribution',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shared.Customer'),
        ),
        migrations.AddField(
            model_name='orderdistribution',
            name='delivery_order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.DeliveryOrder'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdistribution',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=2, help_text='Quantity received on the port in product unit.', max_digits=10, verbose_name='received quantity'),
            preserve_default=False,
        ),
    ]