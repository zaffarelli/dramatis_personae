# Generated by Django 2.1 on 2019-01-10 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0081_auto_20190101_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='onsave_reroll_attributes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='character',
            name='onsave_reroll_skills',
            field=models.BooleanField(default=False),
        ),
    ]
