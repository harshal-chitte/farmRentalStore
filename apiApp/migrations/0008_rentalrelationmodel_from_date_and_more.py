# Generated by Django 4.1.7 on 2023-04-23 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0007_rentalrelationmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="rentalrelationmodel",
            name="from_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="rentalrelationmodel",
            name="to_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
