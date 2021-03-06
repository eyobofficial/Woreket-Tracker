# Generated by Django 2.2.11 on 2020-05-10 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import orders.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchases', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lc_number', models.CharField(max_length=30, verbose_name='letter of credit number')),
                ('vessel', models.CharField(help_text='Shipment vessel name.', max_length=120)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='agreement quantity')),
                ('bill_of_loading', models.CharField(help_text='Bill of loading (B/L) number.', max_length=30)),
                ('arrival_date', models.DateField(verbose_name='vessel arrival date')),
                ('status', models.CharField(choices=[('OPEN', 'open'), ('CLOSED', 'closed')], default='OPEN', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_orders', to='purchases.Batch')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Delivery Order',
                'verbose_name_plural': 'Delivery Orders',
                'ordering': ('-created_at',),
                'permissions': [('close_deliveryorder', 'Close delivery order'), ('reopen_deliveryorder', 'Re-open delivery order')],
                'default_related_name': 'delivery_orders',
            },
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='distributions', to='customers.Customer')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_distributions', to=settings.AUTH_USER_MODEL)),
                ('delivery_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distributions', to='orders.DeliveryOrder')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_distributions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Delivery Order Distribution',
                'verbose_name_plural': 'Delivery Order Distributions',
                'ordering': ('delivery_order', 'created_at'),
                'default_related_name': 'distributions',
                'unique_together': {('delivery_order', 'buyer')},
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('country', django_countries.fields.CountryField(countries=orders.models.NeighbourCountry, max_length=2)),
                ('office', models.CharField(blank=True, max_length=120)),
                ('is_default', models.BooleanField(default=False, verbose_name='default')),
            ],
            options={
                'verbose_name': 'Dispatch Port',
                'verbose_name_plural': 'Dispatch Ports',
                'ordering': ('-is_default', 'name'),
            },
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_orders', to='orders.Port'),
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allocations', to='customers.Customer')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_allocations', to=settings.AUTH_USER_MODEL)),
                ('delivery_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='orders.DeliveryOrder')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_allocations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Delivery Order Allocation',
                'verbose_name_plural': 'Delivery Order Allocations',
                'ordering': ('delivery_order', 'created_at'),
                'default_related_name': 'allocations',
                'unique_together': {('delivery_order', 'buyer')},
            },
        ),
        migrations.CreateModel(
            name='UnionDistribution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.DecimalField(decimal_places=2, help_text='Quantity received by the union in product unit.', max_digits=10, verbose_name='received quantity')),
                ('shortage', models.DecimalField(decimal_places=2, help_text='Quantity deficit after transportation in product unit.', max_digits=10, verbose_name='dispatch shortage')),
                ('over', models.DecimalField(decimal_places=2, help_text='Over quantity supplied in product unit.', max_digits=10, verbose_name='over supplied quantity')),
                ('distribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='union_distributions', to='orders.Distribution')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='union_distributions', to='customers.Location')),
                ('union', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='union_distributions', to='customers.Union')),
            ],
            options={
                'default_related_name': 'union_distributions',
                'order_with_respect_to': 'distribution',
            },
        ),
        migrations.CreateModel(
            name='UnionAllocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.DecimalField(decimal_places=2, help_text='Quantity allocated to the union in product unit.', max_digits=10, verbose_name='allocated quantity')),
                ('allocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='union_allocations', to='orders.Allocation')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='union_allocations', to='customers.Location')),
                ('union', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='union_allocations', to='customers.Union')),
            ],
            options={
                'default_related_name': 'union_allocations',
                'order_with_respect_to': 'allocation',
            },
        ),
    ]
