# Generated by Django 2.2 on 2021-12-18 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0082_specie_vernacular'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='option_display_count',
            field=models.PositiveIntegerField(default=10),
        ),
    ]