# Generated by Django 3.1.1 on 2020-11-03 09:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0011_auto_20201103_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='cut_material',
            name='date_received',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
