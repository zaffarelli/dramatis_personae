# Generated by Django 2.2.7 on 2020-01-14 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0030_auto_20190310_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drama',
            name='players',
        ),
        migrations.RemoveField(
            model_name='event',
            name='foes',
        ),
        migrations.RemoveField(
            model_name='event',
            name='friends',
        ),
    ]