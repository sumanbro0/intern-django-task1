from django.contrib import admin
from django.urls import include, path
from .views import index, movie
urlpatterns = [
    path('', index,name="index"),
    path('<int:id>/', movie,name="movie"),
]