# Generated by Django 2.2 on 2020-10-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0055_character_challenge_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='error',
            field=models.BooleanField(default=False),
        ),
    ]
