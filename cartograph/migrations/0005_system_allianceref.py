# Generated by Django 2.2 on 2021-12-22 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0084_character_audit'),
        ('cartograph', '0004_remove_orbitalitem_speed'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='allianceref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.AllianceRef'),
        ),
    ]
