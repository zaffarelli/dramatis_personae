# Generated by Django 2.2.7 on 2020-04-08 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0037_remove_system_discovered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='discovery',
            field=models.IntegerField(default=6000),
        ),
    ]
