# Generated by Django 4.2.1 on 2023-06-17 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_reading_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='meter',
            name='tariff_rate',
            field=models.DecimalField(decimal_places=2, default=150.0, max_digits=10),
        ),
    ]
