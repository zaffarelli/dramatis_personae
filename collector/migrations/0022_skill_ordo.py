# Generated by Django 2.0.2 on 2018-05-05 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0021_auto_20180505_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='ordo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
