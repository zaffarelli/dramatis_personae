# Generated by Django 2.2 on 2021-11-28 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0077_campaign_known_systems'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='stigma',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
