# Generated by Django 2.2 on 2022-08-17 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('optimizer', '0004_team_campaign'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='public',
            new_name='active',
        ),
    ]