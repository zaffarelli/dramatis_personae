# Generated by Django 4.1.4 on 2023-01-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0023_challenge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['line', 'completion']},
        ),
        migrations.AddField(
            model_name='challenge',
            name='code',
            field=models.CharField(blank=True, default='', max_length=36),
        ),
    ]