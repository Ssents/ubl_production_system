# Generated by Django 3.1 on 2021-03-13 15:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0025_auto_20210313_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coil',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 18, 22, 41, 113678)),
        ),
        migrations.AlterField(
            model_name='coil',
            name='production_transfer_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 18, 22, 41, 113678)),
        ),
    ]
