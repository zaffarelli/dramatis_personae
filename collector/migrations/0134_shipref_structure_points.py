# Generated by Django 3.2 on 2022-11-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0133_auto_20221104_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipref',
            name='structure_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]