# Generated by Django 2.1 on 2019-03-04 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0005_remove_character_species'),
    ]

    operations = [
        migrations.AddField(
            model_name='casteveryman',
            name='attr_mod_balance',
            field=models.IntegerField(default=0),
        ),
    ]