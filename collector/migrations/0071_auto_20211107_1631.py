# Generated by Django 2.2 on 2021-11-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0070_auto_20211107_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='archive_level',
            field=models.CharField(blank=True, choices=[('WKS', 'Workshop'), ('ARK', 'Archive'), ('NON', 'None')], default='NON', max_length=5),
        ),
    ]