# Generated by Django 2.2 on 2021-03-10 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_auto_20210310_0244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloke',
            options={'ordering': ['character', 'level', 'npc'], 'verbose_name': 'FICS: Bloke'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['main_epic', '-main_character'], 'verbose_name': 'References: User Profile'},
        ),
    ]