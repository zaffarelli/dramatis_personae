# Generated by Django 2.2 on 2020-10-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0060_auto_20201004_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='need_pdf',
            field=models.BooleanField(default=False),
        ),
    ]