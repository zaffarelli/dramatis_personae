# Generated by Django 2.2 on 2021-03-27 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0008_auto_20210327_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='tod_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
