# Generated by Django 2.2 on 2022-08-22 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0017_auto_20220822_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='backlog',
            name='keywords',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
    ]