# Generated by Django 3.1 on 2021-03-13 15:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0042_auto_20210313_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='standardmaterial',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 13, 18, 22, 41, 98059)),
        ),
    ]
