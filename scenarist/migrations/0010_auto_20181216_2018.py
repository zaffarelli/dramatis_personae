# Generated by Django 2.1 on 2018-12-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0009_auto_20181216_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drama',
            name='title',
            field=models.CharField(blank=True, default='1544991530.6632857', max_length=128, unique=True),
        ),
    ]
