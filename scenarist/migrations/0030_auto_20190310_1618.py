# Generated by Django 2.1 on 2019-03-10 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0029_auto_20190309_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='to_PDF',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='drama',
            name='to_PDF',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='epic',
            name='to_PDF',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='event',
            name='to_PDF',
            field=models.BooleanField(default=True),
        ),
    ]
