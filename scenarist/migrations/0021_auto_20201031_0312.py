# Generated by Django 2.2 on 2020-10-31 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0020_auto_20201031_0308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizz',
            old_name='side_quest',
            new_name='sidequest',
        ),
    ]