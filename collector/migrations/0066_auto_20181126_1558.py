# Generated by Django 2.0 on 2018-11-26 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0065_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='act',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.Act'),
        ),
        migrations.AlterField(
            model_name='config',
            name='drama',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.Drama'),
        ),
        migrations.AlterField(
            model_name='config',
            name='epic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.Epic'),
        ),
    ]