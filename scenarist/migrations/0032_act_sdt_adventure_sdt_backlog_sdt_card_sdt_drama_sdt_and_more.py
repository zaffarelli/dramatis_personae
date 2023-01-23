# Generated by Django 4.1.4 on 2023-01-16 03:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0031_act_is_ongoing_adventure_is_ongoing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='adventure',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='backlog',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='drama',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='epic',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='scene',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='scheme',
            name='sdt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
