# Generated by Django 2.2 on 2021-12-21 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartograph', '0003_auto_20211107_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orbitalitem',
            name='speed',
        ),
    ]