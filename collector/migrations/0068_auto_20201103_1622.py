# Generated by Django 2.2 on 2020-11-03 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0067_auto_20201022_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloke',
            options={'ordering': ['pc', 'level', 'npc']},
        ),
        migrations.RenameField(
            model_name='bloke',
            old_name='reference',
            new_name='npc',
        ),
        migrations.RenameField(
            model_name='bloke',
            old_name='player',
            new_name='pc',
        ),
    ]
