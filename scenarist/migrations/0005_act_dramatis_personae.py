# Generated by Django 4.1.4 on 2023-04-12 22:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0004_remove_act_action_scene_remove_act_battle_scene_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='dramatis_personae',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), blank=True, null=True, size=None),
        ),
    ]