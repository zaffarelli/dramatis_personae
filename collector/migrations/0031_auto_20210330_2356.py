# Generated by Django 2.2.10 on 2021-03-30 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0030_auto_20210330_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gear',
            name='category',
            field=models.CharField(blank=True, choices=[('0', 'Miscellaneous'), ('1', 'Beverage/Food'), ('2', 'Medical Supplies'), ('3', 'Communications'), ('4', 'Tools'), ('5', 'Think Machines'), ('6', 'Drugs'), ('7', 'Clothing'), ('8', 'Vehicle'), ('9', 'Explosives'), ('10', 'Entertainment'), ('11', 'Weapons'), ('12', 'Armors'), ('13', 'Resources'), ('14', 'Services'), ('15', 'Military Devices'), ('16', 'Power Sources')], default='Miscellaneous', max_length=32, null=True),
        ),
    ]