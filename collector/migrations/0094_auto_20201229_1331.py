# Generated by Django 2.2 on 2020-12-29 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0093_auto_20201229_1330'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='armorref',
            options={'ordering': ['reference'], 'verbose_name': 'FICS: Armor'},
        ),
        migrations.AlterModelOptions(
            name='beneficeafflictionref',
            options={'ordering': ['reference', 'value'], 'verbose_name': 'FICS: Benefice/Affliction'},
        ),
        migrations.AlterModelOptions(
            name='blessingcurseref',
            options={'ordering': ['reference'], 'verbose_name': 'FICS: Blessing/Curse'},
        ),
        migrations.AlterModelOptions(
            name='charactercusto',
            options={'verbose_name': 'FICS: Character Customization'},
        ),
    ]
