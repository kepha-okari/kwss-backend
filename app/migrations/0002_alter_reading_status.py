# Generated by Django 4.2.1 on 2023-06-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Closed')], default=0),
        ),
    ]