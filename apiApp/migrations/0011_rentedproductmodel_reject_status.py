# Generated by Django 4.1.7 on 2023-04-23 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0010_alter_rentedproductmodel_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="rentedproductmodel",
            name="reject_status",
            field=models.BooleanField(default=False),
        ),
    ]
