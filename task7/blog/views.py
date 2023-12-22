

from django.contrib.auth import  login,logout,authenticate
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post

def index(request):
    posts=Post.objects.select_related("author").all()
    return render (request,"index.html",{"posts":posts})






def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect("login")
    return render(request, "signup.html", {})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "login.html", {})




def logout_view(request):
    logout(request)
    return redirect('home')




@login_required
def add_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        pic = request.FILES['pic']
        post = Post(title=title, desc=desc, pic=pic, author=request.user)
        post.save()
        return redirect('home')
    return render(request, 'add_post.html')

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)
    if post.author != request.user:
        return redirect('home')
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        if 'pic' in request.FILES:
            post.pic = request.FILES['pic']
        post.title = title
        post.desc = desc
        post.save()
        return redirect('home')
    return render(request, 'update_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)

    if post.author != request.user:
        return redirect('home')
    post.delete()
    return redirect('home')