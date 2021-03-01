# Generated by Django 3.1 on 2021-01-15 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0025_order_work_order_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.CharField(choices=[('Covermax', 'Covermax'), ('Maxcover', 'Maxcover'), ('IT4', 'IT4'), ('Tekdek', 'Tekdek'), ('Versatile', 'Versatile'), ('Romantile', 'Romantile'), ('Normal Corrugation', 'Normal Corrugation'), ('Plain Sheet', 'Plain Sheet'), ('Normal Ridge', 'Normal Ridge'), ('Versatile Ridge', 'Versatile Ridge'), ('Romantile Ridge', 'Romantile Ridge')], max_length=50)),
                ('gauge', models.IntegerField(choices=[(32, 32), (30, 30), (28, 28), (26, 26), (24, 24), (22, 22), (20, 20)])),
                ('width', models.IntegerField(choices=[(1220, 1220), (975, 975), (960, 960), (487, 487), (462, 462), (320, 320)])),
                ('colour', models.CharField(choices=[('Dark Green', 'Dark Green'), ('Potters Clay', 'Potters Clay'), ('Tile Red', 'Tile Red'), ('Brick Red', 'Brick Red'), ('Maroon', 'Maroon'), ('Zincal', 'Zincal'), ('Service Grey', 'Service Grey'), ('Galvanized Iron', 'Galvanized Iron'), ('Avocado', 'Avocado'), ('Lagoon', 'Lagoon'), ('Sky Blue', 'Sky Blue'), ('Charcoal Black', 'Charcoal Black'), ('Chocolate', 'Chocolate')], max_length=50)),
                ('finish', models.CharField(choices=[('Matt', 'Matt'), ('Plain', 'Plain')], max_length=50)),
                ('total_production', models.IntegerField()),
                ('on_floor_quantity', models.IntegerField()),
                ('transferred_quantity', models.IntegerField()),
                ('shipped_quantity', models.IntegerField()),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 1, 15, 12, 29, 15, 707520))),
            ],
        ),
    ]
