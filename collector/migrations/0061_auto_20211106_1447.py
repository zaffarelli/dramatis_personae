# Generated by Django 2.2 on 2021-11-06 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0060_auto_20211103_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('NON', 'None'), ('ARK', 'Archive'), ('WKS', 'Workshop')], default='NON', max_length=5),
        ),
    ]
