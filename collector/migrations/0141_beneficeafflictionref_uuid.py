# Generated by Django 2.2 on 2021-02-16 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0140_auto_20210216_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficeafflictionref',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]
