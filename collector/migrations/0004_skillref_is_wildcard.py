# Generated by Django 2.2.7 on 2019-12-31 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_auto_20191231_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillref',
            name='is_wildcard',
            field=models.BooleanField(default=False),
        ),
    ]