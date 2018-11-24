# Generated by Django 2.0.6 on 2018-08-02 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0055_beneficeafflictionref_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeneficeAffliction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ba_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.BeneficeAfflictionRef')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collector.Character')),
            ],
        ),
    ]