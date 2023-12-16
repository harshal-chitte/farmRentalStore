# Generated by Django 4.1.7 on 2023-04-23 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("apiApp", "0006_rentedproductmodel_p_renter_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="RentalRelationModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "p_owner",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="r_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "p_renter",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="r_renter",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "r_product",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="r_product",
                        to="apiApp.rentedproductmodel",
                    ),
                ),
            ],
        ),
    ]
