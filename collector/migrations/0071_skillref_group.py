# Generated by Django 2.0 on 2018-12-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0070_auto_20181204_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillref',
            name='group',
            field=models.CharField(choices=[('EDU', 'Education'), ('FIG', 'Combat'), ('AWA', 'Awareness'), ('BOD', 'Physical'), ('TIN', 'Tinkering'), ('PER', 'Performance'), ('SOC', 'Social'), ('CON', 'Control')], default='EDU', max_length=3),
        ),
    ]
