# Generated by Django 3.1 on 2021-01-10 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quality', '0010_coil'),
    ]

    operations = [
        migrations.AddField(
            model_name='coil',
            name='final_mass',
            field=models.IntegerField(default=35),
            preserve_default=False,
        ),
    ]
