# Generated by Django 2.2 on 2020-11-08 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0073_character_stories'),
    ]

    operations = [
        migrations.AddField(
            model_name='charactercusto',
            name='watch_roots',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='charactercusto',
            name='wp_used',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
