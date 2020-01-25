# Generated by Django 2.2.7 on 2020-01-09 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0011_beneficeafflictionref_emphasis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficeafflictionref',
            name='category',
            field=models.CharField(choices=[('ba', 'Background'), ('co', 'Community'), ('po', 'Possessions'), ('ri', 'Riches'), ('st', 'Status'), ('cm', 'Combat'), ('oc', 'Occult'), ('ta', 'Talent'), ('ot', 'Other')], default='ot', max_length=2),
        ),
    ]