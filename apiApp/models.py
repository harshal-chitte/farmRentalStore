from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import pytz
from django.core.exceptions import ValidationError
# Create your models here.
class ProductCategory(models.Model):
    category=models.CharField(max_length=200)

class ProductModel(models.Model):
    p_owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True, default=None)
    p_name = models.CharField(max_length=256, null=True, default=None)
    p_desc = models.TextField(null=True, default=None)
    p_img = models.ImageField(upload_to='media',null=True, default=None)
    p_price = models.FloatField(null=True, default=None)
    r_status = models.BooleanField(default=True)
    p_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,null=True, default=None)
    def __str__(self) -> str:
        return self.p_name


class RentedProductModel(models.Model):
    OPTION_CHOICES = [
        ('request_raised', 'Request Raised'),
        ('request_accepted', 'Request Accepted'),
        ('rented', 'Rented Successfully'),
        ('rejected', 'Rejected'),
    ]
    p_owner = models.ForeignKey(
        User, related_name='p_owner', on_delete=models.CASCADE,null=True, default=None
        )
    p_renter = models.ForeignKey(
        User, related_name='p_renter', on_delete=models.CASCADE,null=True, default=None
        )
    product = models.ForeignKey(
        ProductModel, related_name='product', on_delete=models.SET_NULL, null=True, default=None
        )
    p_name = models.CharField(max_length=256)
    p_desc = models.TextField()
    p_img = models.ImageField(upload_to='media')
    p_price = models.FloatField()
    from_date = models.DateTimeField(default=timezone.now,null=True)
    to_date = models.DateTimeField(default=timezone.now,null=True)
    rent_status = models.CharField(max_length=200, choices=OPTION_CHOICES, default='request_raised')

    def __str__(self) -> str:
        return self.p_name

    def clean(self):
        """
        Validates that there are no overlapping rented products for the same owner and renter.
        """
        # Check if there's already a rented product with the same owner, renter, and overlapping dates.
        existing_rented_product = RentedProductModel.objects.filter(
            p_owner=self.p_owner,
            p_renter=self.p_renter,
            product=self.product,
            from_date__lt=self.to_date,
            to_date__gt=self.from_date,
        ).exclude(id=self.id).first()
        

        if existing_rented_product:
            raise ValidationError(
                f"A rented product with name '{existing_rented_product.p_name}' already exists for the same owner and renter with overlapping dates."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Run validation check before saving
        super().save(*args, **kwargs)

    