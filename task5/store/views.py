from django.shortcuts import get_object_or_404, redirect, render

from .models import Product,Comments

from .forms import CommentForm, ProductForm

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

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    comments = Comments.objects.filter(product=product)
    form = CommentForm()
    return render(request, 'product_detail.html', {'product': product, 'comments': comments, 'form': form})


def add_comment(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            Comments.objects.create(text=text, product=product)
            return redirect('product_detail', id=product.id)

    return redirect('product_detail', id=product.id)


def delete_comment(request, id):
    comment = get_object_or_404(Comments, pk=id)
    product_id = comment.product.id
    comment.delete()
    return redirect('product_detail', id=product_id)


def update_comment(request, id):
    comment = get_object_or_404(Comments, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('product_detail', id=comment.product.id)
    else:
        form = CommentForm(initial={'text': comment.text})
    return render(request,'ss.html', {"form":form})