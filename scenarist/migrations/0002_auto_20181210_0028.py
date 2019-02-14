# Generated by Django 2.1 on 2018-12-10 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('date', models.CharField(max_length=64)),
                ('place', models.CharField(max_length=64)),
                ('friends', models.TextField(blank=True, default='', max_length=640)),
                ('foes', models.TextField(blank=True, default='', max_length=640)),
                ('narrative', models.TextField(blank=True, default='', max_length=640)),
                ('resolution', models.TextField(blank=True, default='', max_length=640)),
            ],
            options={
                'ordering': ['date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Drama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, default='', max_length=64)),
                ('place', models.CharField(blank=True, default='', max_length=64)),
                ('chapter', models.CharField(blank=True, default='', max_length=64)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('title', models.CharField(blank=True, default='', max_length=128, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=640)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('is_public', models.BooleanField(default=True)),
                ('is_editable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['epic', 'chapter', 'date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Epic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('era', models.IntegerField(blank=True, default=5017)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('title', models.CharField(blank=True, default='', max_length=128, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=640)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('is_public', models.BooleanField(default=True)),
                ('is_editable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['era', 'title'],
            },
        ),
        migrations.AddField(
            model_name='drama',
            name='epic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Epic'),
        ),
        migrations.AddField(
            model_name='act',
            name='drama',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Drama'),
        ),
        migrations.AddField(
            model_name='event',
            name='drama',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.Act'),
        ),
    ]