# Generated by Django 2.2.10 on 2021-04-04 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0033_auto_20210404_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='weaponcusto',
            name='ammoes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weaponcusto',
            name='weapon_of_choice',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
