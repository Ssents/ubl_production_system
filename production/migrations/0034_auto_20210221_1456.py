# Generated by Django 3.1 on 2021-02-21 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0033_auto_20210208_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialrequest',
            name='shift',
        ),
        migrations.AlterField(
            model_name='standardmaterial',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 21, 14, 56, 28, 763001)),
        ),
    ]
