# Generated by Django 3.1 on 2021-01-15 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0008_auto_20210110_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coil',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 15, 12, 29, 15, 718513)),
        ),
        migrations.AlterField(
            model_name='coil',
            name='production_transfer_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 15, 12, 29, 15, 718513)),
        ),
    ]
