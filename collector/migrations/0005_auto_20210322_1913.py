# Generated by Django 2.2 on 2021-03-22 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0004_auto_20210311_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='combat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='mental',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='physical',
            field=models.IntegerField(default=0),
        ),
    ]