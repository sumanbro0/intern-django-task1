from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Book)
admin.site.register(models.Cart)
admin.site.register(models.Address)
admin.site.register(models.Order)
admin.site.register(models.Wishlist)
admin.site.register(models.Review)
admin.site.register(models.Notification)
