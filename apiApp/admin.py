from django.contrib import admin
from apiApp import models

admin.site.register(models.ProductModel)
admin.site.register(models.RentedProductModel)
admin.site.register(models.ProductCategory)
