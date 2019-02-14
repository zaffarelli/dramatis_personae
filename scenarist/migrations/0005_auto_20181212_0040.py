# Generated by Django 2.1 on 2018-12-12 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0004_drama_players'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='antagonists',
            new_name='foes',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='protagonists',
            new_name='friends',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='description',
            new_name='resolution',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='description',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='is_editable',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='drama',
            name='population_count',
        ),
        migrations.RemoveField(
            model_name='event',
            name='gamemaster',
        ),
        migrations.RemoveField(
            model_name='event',
            name='population_count',
        ),
        migrations.AddField(
            model_name='drama',
            name='foes',
            field=models.TextField(blank=True, default='', max_length=640),
        ),
        migrations.AddField(
            model_name='drama',
            name='friends',
            field=models.TextField(blank=True, default='', max_length=640),
        ),
        migrations.AddField(
            model_name='drama',
            name='narrative',
            field=models.TextField(blank=True, default='', max_length=1280),
        ),
        migrations.AddField(
            model_name='drama',
            name='resolution',
            field=models.TextField(blank=True, default='', max_length=640),
        ),
        migrations.AddField(
            model_name='event',
            name='narrative',
            field=models.TextField(blank=True, default='', max_length=1280),
        ),
        migrations.AlterField(
            model_name='act',
            name='narrative',
            field=models.TextField(blank=True, default='', max_length=1280),
        ),
    ]