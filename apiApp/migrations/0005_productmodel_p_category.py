# Generated by Django 4.1.7 on 2023-04-23 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0004_alter_productmodel_r_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="productmodel",
            name="p_category",
            field=models.CharField(default=None, max_length=256, null=True),
        ),
    ]
