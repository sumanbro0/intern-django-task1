from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author= models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title