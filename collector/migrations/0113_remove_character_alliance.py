# Generated by Django 2.2 on 2022-05-24 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0112_character_alliance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='alliance',
        ),
    ]