# Generated by Django 2.2.11 on 2020-05-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=60),
        ),
    ]
