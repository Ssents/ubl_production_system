# Generated by Django 3.1.1 on 2020-11-03 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0009_auto_20201102_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cut_Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coil_number', models.CharField(max_length=50)),
                ('initial_mass', models.IntegerField()),
                ('final_mass', models.IntegerField()),
                ('new_or_used', models.BooleanField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='production.order')),
            ],
        ),
    ]
