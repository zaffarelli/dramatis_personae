# Generated by Django 2.2.10 on 2020-06-04 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0037_auto_20200604_0031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ritualcusto',
            old_name='ritual_ref',
            new_name='reference',
        ),
    ]
