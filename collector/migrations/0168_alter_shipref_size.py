# Generated by Django 3.2 on 2022-12-03 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0167_shipref_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipref',
            name='size',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
    ]