# Generated by Django 3.1 on 2021-04-17 08:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0049_auto_20210417_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='section',
        ),
        migrations.AlterField(
            model_name='standardmaterial',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 11, 49, 27, 432545)),
        ),
    ]
