# Generated by Django 2.2 on 2021-03-11 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_auto_20210310_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloke',
            name='level',
            field=models.IntegerField(choices=[(-2, 'Minimal'), (-1, 'Light'), (0, 'Mild'), (1, 'Important'), (2, 'Strong'), (3, 'Maximal')], default=0),
        ),
    ]