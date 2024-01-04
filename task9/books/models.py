from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    price=models.IntegerField()
    desc=models.TextField()
    image=models.ImageField(upload_to="books/images",default="",null=True,blank=True)
    file=models.FileField(upload_to="books/files",default="",null=True,blank=True)



    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    total=models.IntegerField()
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    STATUS_CHOICES=(
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('delivered','delivered'),
        ('cancelled','cancelled')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ManyToManyField(Cart)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    total=models.IntegerField()
    status=models.CharField(max_length=100,default="pending",choices=STATUS_CHOICES)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    comment=models.TextField()
    rating=models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    book_url=models.URLField(blank=True,null=True,default="")

    def __str__(self):
        return self.user.username