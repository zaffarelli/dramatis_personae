# Generated by Django 3.2 on 2022-12-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0171_character_use_only_entrance'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='age_offset',
            field=models.IntegerField(default=0),
        ),
    ]
