# Generated by Django 2.2.10 on 2020-09-22 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0054_auto_20200728_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='challenge_value',
            field=models.IntegerField(default=0),
        ),
    ]