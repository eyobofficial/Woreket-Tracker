# Generated by Django 2.2.11 on 2020-05-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0002_supplier_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='short_name',
            field=models.CharField(blank=True, max_length=60, verbose_name='abbreviation'),
        ),
    ]
