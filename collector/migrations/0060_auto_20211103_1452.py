# Generated by Django 2.2 on 2021-11-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0059_auto_20211103_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('WKS', 'Workshop'), ('NON', 'None'), ('ARK', 'Archive')], default='NON', max_length=5),
        ),
    ]
