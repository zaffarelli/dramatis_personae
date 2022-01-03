# Generated by Django 2.2 on 2021-12-31 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0093_auto_20211231_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='armorref',
            name='material_connected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='material_fabric',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='material_light',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='material_metal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='material_powered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='material_reinforced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='material_synth',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='armorref',
            name='origins',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='armorref',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='armorref',
            name='sa_sp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='armorref',
            name='to_sp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='armorref',
            name='wa_sp',
            field=models.IntegerField(default=0),
        ),
    ]
