# Generated by Django 2.2.11 on 2020-05-04 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200504_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allocation',
            name='quantity',
        ),
    ]
