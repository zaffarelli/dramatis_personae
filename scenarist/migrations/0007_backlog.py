# Generated by Django 2.2 on 2022-08-19 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0006_adventure'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=256, unique=True)),
                ('chapter', models.CharField(blank=True, default='0', max_length=64)),
                ('date', models.CharField(blank=True, default='', max_length=128)),
                ('place', models.CharField(blank=True, default='', max_length=128)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('visible', models.BooleanField(default=True)),
                ('battle_scene', models.BooleanField(default=False)),
                ('chase_scene', models.BooleanField(default=False)),
                ('action_scene', models.BooleanField(default=False)),
                ('technical_scene', models.BooleanField(default=False)),
                ('spiritual_scene', models.BooleanField(default=False)),
                ('political_scene', models.BooleanField(default=False)),
                ('downtime_scene', models.BooleanField(default=False)),
                ('to_PDF', models.BooleanField(default=True)),
                ('full_id', models.CharField(blank=True, default='', max_length=64)),
                ('description', models.TextField(blank=True, default='', max_length=6000)),
                ('rewards', models.TextField(blank=True, default='', max_length=1024)),
                ('card_type', models.CharField(choices=[('UN', 'Uncategorized'), ('SC', 'Scene'), ('EV', 'Event'), ('BK', 'Background')], default='UN', max_length=2)),
                ('resolution', models.TextField(blank=True, default='', max_length=2560)),
                ('challenge', models.PositiveIntegerField(default=1)),
                ('anchor', models.CharField(blank=True, default='', max_length=256)),
                ('act', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Act')),
            ],
            options={
                'ordering': ['chapter', 'title'],
            },
        ),
    ]