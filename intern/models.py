from django.db import models

# Create your models here.

categories=[("Electronics", "Electronics"),("Clothes","Clothes"),("Grocesery","Grocesery")]

class Product(models.Model):
    title=models.CharField(max_length=255)
    category=models.CharField(choices=categories,max_length=50)
    image= models.ImageField(upload_to='product_images/')
    desc=models.TextField(max_length=555)

    def __str__(self):
        return self.title