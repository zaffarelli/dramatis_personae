# Generated by Django 2.0.2 on 2018-06-06 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0035_auto_20180602_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shield',
            name='charges',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]