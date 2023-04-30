# Generated by Django 2.2 on 2021-11-07 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0063_auto_20211107_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('ARK', 'Archive'), ('NON', 'None'), ('WKS', 'Workshop')], default='NON', max_length=5),
        ),
    ]