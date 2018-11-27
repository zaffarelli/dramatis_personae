# Generated by Django 2.0 on 2018-11-25 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0061_character_epic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=64)),
                ('place', models.CharField(max_length=64)),
                ('population_count', models.IntegerField(blank=True, default=0)),
                ('title', models.CharField(blank=True, default='', max_length=128, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=128)),
                ('gamemaster', models.CharField(blank=True, default='zaffarelli@gmail.com', max_length=128)),
                ('is_public', models.BooleanField(default=True)),
                ('is_editable', models.BooleanField(default=True)),
                ('epic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='collector.Epic')),
            ],
        ),
        migrations.AlterModelOptions(
            name='armorref',
            options={'ordering': ['reference']},
        ),
        migrations.AlterModelOptions(
            name='blessingcurse',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='shieldref',
            options={'ordering': ['reference']},
        ),
        migrations.AlterModelOptions(
            name='skillref',
            options={'ordering': ['reference']},
        ),
        migrations.AlterModelOptions(
            name='talent',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='weaponref',
            options={'ordering': ['reference']},
        ),
        migrations.RemoveField(
            model_name='act',
            name='epic',
        ),
        migrations.AddField(
            model_name='act',
            name='drama',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='collector.Drama'),
        ),
    ]