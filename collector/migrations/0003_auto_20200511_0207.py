# Generated by Django 2.2.10 on 2020-05-11 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_auto_20200510_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipref',
            name='ship_engines',
            field=models.CharField(blank=True, choices=[('1', 'Slow'), ('2', 'Standard'), ('3', 'Fast')], default='Standard', max_length=30),
        ),
        migrations.AlterField(
            model_name='shipref',
            name='ship_shields',
            field=models.CharField(blank=True, choices=[('0', '2/2'), ('1', '4/4'), ('2', '6/6'), ('3', '8/8'), ('4', '9/9'), ('5', '12/12')], default='Standard', max_length=30),
        ),
        migrations.AlterField(
            model_name='shipsection',
            name='section',
            field=models.CharField(blank=True, choices=[('0', 'Bridge'), ('1', 'Maneuver'), ('2', 'Gundeck'), ('3', 'Engine Room'), ('4', 'Marines Deck'), ('5', 'Turret A'), ('6', 'Turret B'), ('7', 'Turret Z'), ('8', 'Spinal Mount'), ('9', 'Shieldbank'), ('10', 'Troop Quarters')], default='Bridge', max_length=30, null=True),
        ),
    ]