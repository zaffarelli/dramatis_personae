# Generated by Django 4.1.4 on 2023-03-16 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0126_campaign_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='short_name',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
