# Generated by Django 2.2 on 2021-11-03 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0046_auto_20211102_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('ARK', 'Archive'), ('WKS', 'Workshop'), ('NON', 'None')], default='NON', max_length=5),
        ),
    ]