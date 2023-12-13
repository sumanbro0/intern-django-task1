from django.shortcuts import render
from .models import Author, Book
# Create your views here.
def index(request):
    books=Book.objects.all()
    authors=Author.objects.all()
    aut=authors[0].books.all()
    return render(request,"index.html",{"books":books,"authors":authors})