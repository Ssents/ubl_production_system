# Generated by Django 3.1.1 on 2020-10-03 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_name', models.CharField(max_length=50)),
                ('machine_number', models.CharField(max_length=50)),
                ('machine_serial_number', models.CharField(max_length=50)),
                ('machine_photo', models.ImageField(upload_to='photos/maintenance/machines/%Y/%m/%d/')),
                ('machine_hourly_capacity', models.IntegerField()),
                ('section', models.CharField(choices=[('WIRE', 'Wire Section'), ('ROOFING', 'Roofing Section'), ('SMD', 'Steel Merchandise division')], default='ROOFING', max_length=50)),
            ],
            options={
                'ordering': ['-section', '-machine_name', '-machine_serial_number'],
            },
        ),
    ]
