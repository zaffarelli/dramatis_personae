# Generated by Django 2.2.7 on 2019-12-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0026_skillcusto'),
    ]

    operations = [
        migrations.AddField(
            model_name='charactercusto',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]