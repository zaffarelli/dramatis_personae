# Generated by Django 4.1.4 on 2023-04-12 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0003_remove_card_sublevels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='act',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='act',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='adventure',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='event',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='technical_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='action_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='battle_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='business_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='chase_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='downtime_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='mystery_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='political_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='roleplay_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='spiritual_scene',
        ),
        migrations.RemoveField(
            model_name='scheme',
            name='technical_scene',
        ),
    ]