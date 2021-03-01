# Generated by Django 3.1 on 2021-01-21 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0012_auto_20210117_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('colour', models.CharField(max_length=50)),
                ('finish', models.CharField(max_length=50)),
                ('gauge', models.IntegerField()),
                ('width', models.IntegerField()),
                ('bond_inventory', models.IntegerField()),
                ('transferred', models.IntegerField()),
                ('production_stock', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='coil',
            name='date_received',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 21, 14, 16, 0, 491033)),
        ),
        migrations.AlterField(
            model_name='coil',
            name='production_transfer_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 21, 14, 16, 0, 491033)),
        ),
    ]
