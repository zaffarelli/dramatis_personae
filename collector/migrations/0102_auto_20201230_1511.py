# Generated by Django 2.2 on 2020-12-30 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scenarist', '0022_auto_20201107_1339'),
        ('collector', '0101_config_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='aaa', max_length=128, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=128)),
                ('is_active', models.BooleanField(default=False)),
                ('smart_code', models.CharField(blank=True, default='xxxxxx', max_length=6)),
                ('color_front', models.CharField(default='#00F0F0F0', max_length=9)),
                ('color_back', models.CharField(default='#00101010', max_length=9)),
                ('color_linkup', models.CharField(default='#00801080', max_length=9)),
                ('color_linkdown', models.CharField(default='#00401040', max_length=9)),
                ('color_counterback', models.CharField(default='#00404040', max_length=9)),
                ('logo', models.CharField(default='nologo.png', max_length=128)),
                ('current_drama', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scenarist.Drama')),
                ('epic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scenarist.Epic')),
                ('gm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('rpgsystem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collector.RpgSystem')),
            ],
            options={
                'verbose_name': 'References: Campaign Config',
                'ordering': ['title', 'epic'],
            },
        ),
        migrations.DeleteModel(
            name='Config',
        ),
    ]
