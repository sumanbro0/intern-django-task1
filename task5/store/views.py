from django.shortcuts import redirect, render

from .models import Product

from .forms import ProductForm

# Create your views here.
def index(request):
    products=Product.objects.all()
    return render(request, "index.html", {"products":products})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data["name"]
            price=form.cleaned_data["price"]
            description=form.cleaned_data["description"]
            image=form.cleaned_data["image"]
            product=Product(name=name,price=price,description=description,image=image)
            product.save()
            return redirect("index")
    else:
        form = ProductForm()

    return render(request, "add_products.html", {"form": form})

def product_detail(request,id):
    product=Product.objects.get(id=id)
    return render(request, "product_detail.html", {"product":product})