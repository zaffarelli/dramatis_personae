# Generated by Django 2.0 on 2018-12-04 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0069_beneficeaffliction_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weaponref',
            options={'ordering': ['category', 'damage_class', 'reference']},
        ),
        migrations.AddField(
            model_name='character',
            name='armor_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='shield_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='weapon_cost',
            field=models.IntegerField(default=0),
        ),
    ]
