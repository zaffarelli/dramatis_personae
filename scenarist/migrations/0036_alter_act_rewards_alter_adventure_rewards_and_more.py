# Generated by Django 4.1.4 on 2023-04-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0035_act_dramatis_personae_adventure_dramatis_personae_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='adventure',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='backlog',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='card',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='drama',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='epic',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='event',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='scene',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='scheme',
            name='rewards',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
    ]
