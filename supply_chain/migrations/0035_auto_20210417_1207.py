# Generated by Django 3.1 on 2021-04-17 09:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0034_auto_20210417_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coil',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 12, 7, 17, 877048)),
        ),
        migrations.AlterField(
            model_name='coil',
            name='production_transfer_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 12, 7, 17, 877048)),
        ),
    ]
