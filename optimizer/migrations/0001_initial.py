# Generated by Django 4.1.4 on 2023-04-15 13:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.campaign')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TeamMate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.character')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizer.team')),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('is_armored', models.BooleanField(blank=True, default=False)),
                ('is_armed', models.BooleanField(blank=True, default=False)),
                ('is_balanced', models.BooleanField(blank=True, default=False)),
                ('has_species_lifepath', models.BooleanField(default=False)),
                ('has_standard_lifepath', models.BooleanField(default=False)),
                ('has_tods_lifepath', models.BooleanField(default=False)),
                ('is_applied', models.BooleanField(blank=True, default=False)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date published')),
                ('last_comment', models.TextField(blank=True, default='', max_length=1024)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.character')),
            ],
            options={
                'verbose_name': 'Optimizer: Character Policy',
                'ordering': ['name'],
            },
        ),
    ]
