# Generated by Django 4.1.4 on 2023-03-16 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0125_alter_character_birthdate_alter_character_caste_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='short_name',
            field=models.TextField(blank=True, default='', max_length=64),
        ),
    ]
