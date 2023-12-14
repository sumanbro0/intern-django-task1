from django.db import models

# Create your models here.



class Tag(models.Model):
    tag=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.tag


class Director(models.Model):
    name=models.CharField(max_length=255)
    bio=models.TextField()
    
    def __str__(self) -> str:
        return self.name

class Cast(models.Model):
    actors=models.CharField(max_length=255)
    director=models.ForeignKey(Director,on_delete=models.CASCADE,related_name="casts",null=True)

    def __str__(self) -> str:
        return str(self.id)

class Movie(models.Model):
    name=models.CharField(max_length=255)
    desc=models.TextField()
    tags=models.ManyToManyField(Tag,related_name="movies")
    cast=models.ForeignKey(Cast,on_delete=models.CASCADE,related_name="movies",null=True)

    def __str__(self) -> str:
        return self.name

