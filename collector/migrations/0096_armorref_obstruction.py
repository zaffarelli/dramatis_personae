# Generated by Django 2.2 on 2021-12-31 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0095_armorref_material_plastic'),
    ]

    operations = [
        migrations.AddField(
            model_name='armorref',
            name='obstruction',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
