# Generated by Django 4.1.7 on 2023-04-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0003_productmodel_r_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmodel",
            name="r_status",
            field=models.BooleanField(default=True),
        ),
    ]