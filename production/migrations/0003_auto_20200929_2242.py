# Generated by Django 3.1.1 on 2020-09-29 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_auto_20200927_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
