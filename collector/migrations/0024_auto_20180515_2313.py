# Generated by Django 2.0.2 on 2018-05-15 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0023_character_alliancehash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weaponref',
            name='reference',
            field=models.CharField(blank=True, default='', max_length=64, unique=True),
        ),
    ]
