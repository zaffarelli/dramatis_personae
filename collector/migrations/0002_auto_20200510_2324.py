# Generated by Django 2.2.10 on 2020-05-10 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipref',
            name='ship_class',
            field=models.CharField(blank=True, choices=[('0', 'Fighter'), ('1', 'Shuttle'), ('2', 'Bomber'), ('3', 'Explorer'), ('4', 'Raider'), ('5', 'Escort'), ('6', 'Frigate'), ('7', 'Galliot'), ('8', 'Fast Freighter'), ('9', 'Small Freighter'), ('10', 'Assault Lander'), ('11', 'Destroyer'), ('12', 'Cruiser'), ('13', 'Large Freighter'), ('14', 'Luxury Liner'), ('15', 'Dreadnough'), ('16', 'Carrier')], default='Shuttle', max_length=30),
        ),
    ]
