# Generated by Django 5.0.3 on 2024-06-15 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='total_Seats',
            field=models.FloatField(default=34),
        ),
    ]
