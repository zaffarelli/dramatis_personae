# Generated by Django 2.2 on 2021-11-07 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0062_auto_20211106_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('NON', 'None'), ('WKS', 'Workshop'), ('ARK', 'Archive')], default='NON', max_length=5),
        ),
    ]