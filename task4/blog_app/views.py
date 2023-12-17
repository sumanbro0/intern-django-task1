from django.shortcuts import render
from .models import Post, Tag
# Create your views here.
def index(request):
    posts = Post.objects.prefetch_related("tags").all()
    return render(request, 'index.html',{"posts":posts})



def post_detail(request, post_id):
    post = Post.objects.prefetch_related("tags").get(id=post_id)
    return render(request, 'post_detail.html',{"post":post})

# add new post from client side
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.POST.get("author")
        tags = request.POST.get("tags")
        post = Post.objects.create(title=title, content=content, author=author)

        tag_names = tags.split() 
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)  
            post.tags.add(tag)  
        post.save()
        return render(request, 'add_post.html',{"post":post})
    return render(request, 'add_post.html')