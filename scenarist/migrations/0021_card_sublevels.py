# Generated by Django 4.1.4 on 2023-01-03 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0020_card_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='sublevels',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]