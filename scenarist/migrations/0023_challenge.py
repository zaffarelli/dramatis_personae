# Generated by Django 4.1.4 on 2023-01-04 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenarist', '0022_alter_card_sublevels'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.CharField(blank=True, default='', max_length=256)),
                ('completion', models.PositiveIntegerField(blank=True, default=1)),
                ('plot_card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarist.card')),
            ],
            options={
                'ordering': ['completion'],
            },
        ),
    ]
