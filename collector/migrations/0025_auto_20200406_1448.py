# Generated by Django 2.2.7 on 2020-04-06 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0024_auto_20200406_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system',
            name='jump_road_to',
        ),
        migrations.AddField(
            model_name='system',
            name='jump_road_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='_system_jump_road_to_+', to='collector.System'),
        ),
    ]
