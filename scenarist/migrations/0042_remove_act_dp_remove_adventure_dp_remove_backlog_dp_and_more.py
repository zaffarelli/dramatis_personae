# Generated by Django 4.1.4 on 2023-04-10 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0041_alter_act_dp_alter_adventure_dp_alter_backlog_dp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='act',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='card',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='dp',
        ),
    ]
