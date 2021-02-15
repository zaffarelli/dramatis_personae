# Generated by Django 2.2 on 2021-02-13 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0124_character_alliance_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='alias',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='character',
            name='alliance',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='character',
            name='faction',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
