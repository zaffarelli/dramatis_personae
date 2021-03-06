# Generated by Django 2.2.7 on 2020-02-29 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=256, unique=True)),
                ('chapter', models.CharField(blank=True, default='', max_length=64)),
                ('date', models.CharField(blank=True, default='', max_length=128)),
                ('place', models.CharField(blank=True, default='', max_length=128)),
                ('description', models.TextField(blank=True, default='', max_length=2560)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('to_PDF', models.BooleanField(default=True)),
                ('resolution', models.TextField(blank=True, default='', max_length=2560)),
            ],
            options={
                'ordering': ['chapter', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Epic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=256, unique=True)),
                ('chapter', models.CharField(blank=True, default='', max_length=64)),
                ('date', models.CharField(blank=True, default='', max_length=128)),
                ('place', models.CharField(blank=True, default='', max_length=128)),
                ('description', models.TextField(blank=True, default='', max_length=2560)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('to_PDF', models.BooleanField(default=True)),
                ('era', models.IntegerField(blank=True, default=5017)),
                ('shortcut', models.CharField(blank=True, default='xx', max_length=32)),
                ('image', models.CharField(blank=True, default='', max_length=64)),
                ('system', models.CharField(blank=True, default='', max_length=128, null=True)),
            ],
            options={
                'ordering': ['era', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=256, unique=True)),
                ('chapter', models.CharField(blank=True, default='', max_length=64)),
                ('date', models.CharField(blank=True, default='', max_length=128)),
                ('place', models.CharField(blank=True, default='', max_length=128)),
                ('description', models.TextField(blank=True, default='', max_length=2560)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('to_PDF', models.BooleanField(default=True)),
                ('resolution', models.TextField(blank=True, default='', max_length=2560)),
                ('challenge', models.PositiveIntegerField(default=1)),
                ('anchor', models.CharField(blank=True, default='', max_length=256)),
                ('act', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Act')),
            ],
            options={
                'ordering': ['chapter', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Drama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=256, unique=True)),
                ('chapter', models.CharField(blank=True, default='', max_length=64)),
                ('date', models.CharField(blank=True, default='', max_length=128)),
                ('place', models.CharField(blank=True, default='', max_length=128)),
                ('description', models.TextField(blank=True, default='', max_length=2560)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('to_PDF', models.BooleanField(default=True)),
                ('resolution', models.TextField(blank=True, default='', max_length=2560)),
                ('epic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Epic')),
            ],
            options={
                'ordering': ['epic', 'chapter', 'date', 'title'],
            },
        ),
        migrations.AddField(
            model_name='act',
            name='drama',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Drama'),
        ),
    ]
