# Generated by Django 3.2 on 2022-12-03 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0168_alter_shipref_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipref',
            old_name='size',
            new_name='size_rating',
        ),
    ]
