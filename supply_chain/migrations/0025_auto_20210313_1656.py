# Generated by Django 3.1 on 2021-03-13 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0024_auto_20210310_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coil',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 16, 56, 9, 214248)),
        ),
        migrations.AlterField(
            model_name='coil',
            name='production_transfer_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 16, 56, 9, 214248)),
        ),
    ]
