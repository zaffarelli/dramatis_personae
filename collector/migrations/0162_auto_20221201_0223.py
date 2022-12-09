# Generated by Django 3.2 on 2022-12-01 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0161_auto_20221201_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipsystemslot',
            name='power_consumption',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='shipsystemslot',
            name='power_stack',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
