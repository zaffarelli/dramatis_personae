# Generated by Django 2.1 on 2018-12-10 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0079_auto_20181210_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='act',
        ),
        migrations.RemoveField(
            model_name='config',
            name='drama',
        ),
    ]
