# Generated by Django 3.2 on 2022-12-01 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0156_shipref_cs_power_stack'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipref',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
