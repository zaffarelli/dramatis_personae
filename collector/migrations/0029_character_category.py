# Generated by Django 2.0.2 on 2018-05-17 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0028_skillref_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='category',
            field=models.CharField(choices=[('none', 'None'), ('villain', 'Bad guy'), ('hero', 'Good guy')], default='none', max_length=16),
        ),
    ]