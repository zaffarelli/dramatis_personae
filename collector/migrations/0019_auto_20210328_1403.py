# Generated by Django 2.2 on 2021-03-28 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0018_auto_20210328_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyberfeature',
            name='need_fix',
        ),
        migrations.RemoveField(
            model_name='cyberfeature',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='cyberwareref',
            name='need_fix',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]