# Generated by Django 2.1 on 2019-03-03 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_auto_20190303_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='casteveryman',
            name='description',
            field=models.TextField(blank=True, default='', max_length=512),
        ),
    ]