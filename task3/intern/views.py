from django.shortcuts import render
from .models import Cast, Director, Movie
# Create your views here.
def index(request):
    directors=Director.objects.all()    
    return render(request,'index.html',{"directors":directors})


def movie(request,id):
    dir_with_cast_n_movies = Director.objects.prefetch_related("casts","casts__movies").get(id=id)
    # movies=Movie.objects.select_related("cast").get(id=id)

    # print(movies.cast.actors)
    # print(dir.casts.all().first().movies.all().first())
    return render(request,'movie.html',{"director":dir_with_cast_n_movies})