# Generated by Django 3.2 on 2022-11-05 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0151_spaceship_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaceship',
            name='video',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
    ]