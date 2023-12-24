from django.db import models

from django.contrib.auth.hashers import make_password, check_password



# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=255,unique=True)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    otp=models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    
    def set_password(self, password):
        self.password = make_password(password)

    def get_password(self, password):
        return check_password(password, self.password)


        
    
class Post(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField()
    pic = models.ImageField(upload_to='thumbnails/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.title
    
