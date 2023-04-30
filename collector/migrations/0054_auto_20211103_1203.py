# Generated by Django 2.2 on 2021-11-03 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0053_auto_20211103_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('WKS', 'Workshop'), ('ARK', 'Archive'), ('NON', 'None')], default='NON', max_length=5),
        ),
    ]