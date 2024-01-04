from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from .mail import send_verification
from .models import Address, Book, Cart, Notification, Order, Review, Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.postgres.search import SearchVector


# Create your views here.
def index(request):
    books = Book.objects.all()
    context = {'books': books}
    if request.user.is_authenticated:
        wishlist_book_ids = Wishlist.objects.filter(user=request.user).values_list('book', flat=True)
        cart_book_ids = Cart.objects.filter(user=request.user).values_list('book', flat=True)
        orders=Order.objects.filter(user=request.user)
        if len(orders)>=5:
            context.update({'offer':'25% off on all orders'})
        context.update({
            'wishlist_book_ids': wishlist_book_ids,
            'cart_book_ids': cart_book_ids,
        })

    return render(request, 'index.html', context)


def book(request,id):
    book=Book.objects.get(id=id)
    comments=Review.objects.filter(book=book)
    average_rating = 0
    if comments:
        average_rating = sum([i.rating for i in comments]) / len(comments)
    return render(request,'details.html',{'book':book,'comments':comments, 'average_rating': range(int(average_rating))})



def log_in(request):
    msg=request.GET.get('msg')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect("index")
        else:
            messages.error(request,"Invalid Credentials")
            return render(request,'login.html')

    return render(request,'login.html',{'msg':msg})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect("index")    

def sign_up(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        try:
            user=User.objects.create_user(username,email,password)
            user.save()
            messages.success(request,"Account created successfully")
            return redirect("login")
        except:
            messages.error(request,"Username already exists")
            return render(request,'signup.html')
    return render(request,'signup.html')

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            index_url = request.build_absolute_uri(reverse('index'))
            url=f"{index_url}/reset_password/{user.id}"
            send_verification(user.username, user.email, url)
            messages.success(request, "Reset link sent to your email")
            return redirect('login')
        else:
            messages.error(request, "Email doesn't exist")
            return render(request, 'forgot_password.html')
    return render(request, 'forgot_password.html')



def change_password(request, id):
    
    if request.method == "POST":
        password = request.POST.get('new_password')
        user = User.objects.get(id=id)
        user.set_password(password)
        user.save()
        messages.success(request, "Password changed successfully")
        return redirect('login')
    return render(request, 'change_password.html')


@login_required(login_url='login')
def remove_from_cart(request,id):
    book=Book.objects.get(id=id)
    cart = Cart.objects.filter(book=book, user=request.user)
    if cart:
        cart.first().delete()
        messages.success(request,"Book removed from cart")
    else:
        messages.error(request,"Book don't exits")

    return redirect("cart")

@login_required(login_url='login')
def cart(request):
    cart=Cart.objects.filter(user=request.user , ordered=False)
    total=0
    for i in cart:
        total+=i.total
    return render(request,'cart.html',{'items':cart,'total':total})


@login_required(login_url='login')
def add_to_cart(request,id):
    book=Book.objects.get(id=id)
    cart=Cart.objects.create(user=request.user,book=book,quantity=1,price=book.price,total=book.price)
    cart.save()
    messages.success(request,"Book added to cart")

    return redirect("index")

@login_required(login_url='login')
def address(request):
    addresses=Address.objects.filter(user=request.user)
    if request.method=="POST":
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        address=Address.objects.create(user=request.user,address=address,city=city,state=state,pincode=pincode)
        address.save()
        messages.success(request,"Address added successfully")

    return render(request,'address.html',{'addresses':addresses})



@login_required(login_url='login')
def place_order(request):
    addr_id = request.GET.get('address')
    cart = Cart.objects.filter(user=request.user)
    total_price = sum(item.price * item.quantity for item in cart)
    address = Address.objects.get(id=addr_id)
    
    num_orders = Order.objects.filter(user=request.user).count()
    
    if num_orders > 5:
        total_price *= 0.75 
    
    order = Order(user=request.user,address=address,total=total_price,cart=cart)
    order.save()
    for item in cart:
        item.ordered = True
        item.save()
    items = Cart.objects.filter(user=request.user, ordered=True)
    messages.success(request, "Order placed successfully")
    return render(request, 'place_order.html', {'cart': cart, 'total_price': total_price, 'order': order, 'address': address, 'items': items})

@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


def search(request):
    query=request.GET.get('query')
    books=Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(genre__icontains=query) | Q(desc__icontains=query))

    
    # vector = SearchVector('title', 'author', 'genre', 'desc')
    # books = Book.objects.annotate(search=vector).filter(search=query)


    return render(request,'index.html',{'books':books})


@login_required(login_url='login')
def add_to_wishlist(request,id):
    book=Book.objects.get(id=id)
    if not Wishlist.objects.filter(user=request.user, book=book).exists():
        wishlist=Wishlist.objects.create(user=request.user,book=book)
        wishlist.save()
        messages.success(request,"Book added to wishlist")
    else:
        messages.error(request,"Book already in wishlist")

    return redirect("index")

@login_required(login_url='login')
def wishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'wishlists':wishlist})


@login_required(login_url='login')
def remove_from_wishlist(request,id):
    book=Book.objects.get(id=id)
    wishlist = Wishlist.objects.filter(book=book, user=request.user)
    if wishlist:
        wishlist.first().delete()
        messages.success(request,"Book removed from wishlist")
    else:
        messages.error(request,"Book don't exits")

    return redirect("wishlist")


@login_required(login_url='login')
def add_review(request, id):
    book = Book.objects.get(id=id)
    comment = request.POST.get('review')
    rating = request.POST.get('rating')
    review = Review.objects.create(user=request.user, book=book, comment=comment, rating=rating)
    review.save()
    messages.success(request, "Review added successfully")
    return redirect('book_detail', id=id)

@login_required(login_url='login')
def remove_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    messages.success(request, "Review removed successfully")
    return redirect('book_detail', id=review.book.id)



def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})



def delete_notification(request, id):
    notification = Notification.objects.get(id=id)
    notification.delete()
    return redirect('notifications')



@login_required(login_url='login')
def my_books(request):
    orders=Order.objects.prefetch_related("cart").filter(user=request.user,status="delivered")
    books=[]
    for order in orders:
        for item in order.cart.all():
            books.append(item.book)
    return render(request, 'my_books.html',{"books":books})
    


def read_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'read_book.html', {'book': book})