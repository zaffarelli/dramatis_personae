# Generated by Django 4.1.4 on 2023-01-16 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0032_act_sdt_adventure_sdt_backlog_sdt_card_sdt_drama_sdt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='experience',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
