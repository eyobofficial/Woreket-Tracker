# Generated by Django 2.2.11 on 2020-09-20 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20200614_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='year',
            field=models.PositiveIntegerField(choices=[(2010, '2010/2011'), (2011, '2011/2012'), (2012, '2012/2013'), (2013, '2013/2014'), (2014, '2014/2015'), (2015, '2015/2016'), (2016, '2016/2017'), (2017, '2017/2018')]),
        ),
    ]
