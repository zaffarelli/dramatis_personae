# Generated by Django 2.2.10 on 2020-05-11 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0006_auto_20200511_0352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shipref',
            options={'ordering': ('builder', 'size_rating'), 'verbose_name': 'Spacecraft: Ship Reference'},
        ),
    ]
