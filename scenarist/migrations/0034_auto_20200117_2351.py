# Generated by Django 2.2.7 on 2020-01-17 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0033_epic_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='estimated_gametime',
        ),
        migrations.AddField(
            model_name='act',
            name='population_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='drama',
            name='population_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='population_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]