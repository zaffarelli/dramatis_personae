# Generated by Django 2.2 on 2020-11-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0080_orbitalitem_rings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='zoom_factor',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='system',
            name='zoom_val',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
