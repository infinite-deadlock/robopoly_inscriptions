# Generated by Django 3.0.6 on 2020-05-17 21:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inscriptions', '0002_auto_20200517_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='inscription_date_robopoly',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
