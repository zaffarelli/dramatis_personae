# Generated by Django 2.2.10 on 2021-03-29 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0021_auto_20210329_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourofdutyref',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]