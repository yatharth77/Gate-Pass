# Generated by Django 2.2.1 on 2019-05-25 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gatepass_apply', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatepass',
            name='from_date',
            field=models.CharField(default=datetime.datetime(2019, 5, 25, 10, 4, 38, 554081), max_length=30),
        ),
        migrations.AlterField(
            model_name='gatepass',
            name='to_date',
            field=models.CharField(default=datetime.datetime(2019, 5, 25, 10, 4, 38, 554104), max_length=30),
        ),
    ]