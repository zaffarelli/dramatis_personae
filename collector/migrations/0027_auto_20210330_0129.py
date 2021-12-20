# Generated by Django 2.2.10 on 2021-03-29 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0026_auto_20210330_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourofdutyref',
            name='category',
            field=models.CharField(choices=[('0', 'Birthright'), ('10', 'Upbringing'), ('20', 'Apprenticeship'), ('30', 'Early Career'), ('40', 'Tour of Duty'), ('50', 'Worldly Benefits'), ('60', 'Nameless Kit'), ('70', 'Build'), ('80', 'Special')], default='Tour of Duty', max_length=20),
        ),
    ]