# Generated by Django 4.1.7 on 2023-04-23 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("apiApp", "0005_productmodel_p_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="rentedproductmodel",
            name="p_renter",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="p_renter",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="rentedproductmodel",
            name="r_status",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="rentedproductmodel",
            name="p_owner",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="p_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
