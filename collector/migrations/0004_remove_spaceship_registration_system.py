# Generated by Django 4.1.4 on 2023-04-24 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_remove_character_current_fief_remove_character_fief_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spaceship',
            name='registration_system',
        ),
    ]
