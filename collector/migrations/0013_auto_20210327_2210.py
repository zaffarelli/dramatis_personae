# Generated by Django 2.2 on 2021-03-27 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0012_auto_20210327_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourofdutyref',
            name='source',
            field=models.CharField(choices=[('FS2CRB', 'HDi Fading Suns Official'), ('FICS', 'Zaffarelli Fading Suns')], default='FS2CRB', max_length=32),
        ),
    ]
