from django.shortcuts import render

from intern.models import Product

# Create your views here.
def index(request):
    products=Product.objects.all()
    return render(request,"index.html",{"products":products})

def detail(request,id):
    product=Product.objects.get(id=id)
    return render(request,"details.html",{"product":product})

