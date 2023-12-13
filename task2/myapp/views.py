from django.shortcuts import render
from .models import Author, Book
# Create your views here.
def index(request):
    books=Book.objects.all()
    authors=Author.objects.all()
    return render(request,"index.html",{"books":books,"authors":authors})