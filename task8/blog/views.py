from django.views import View
from django.shortcuts import render, redirect
from .models import Comment, Post, User
from django.contrib.auth.hashers import check_password
import random
from .mail import send_otp

from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from django.shortcuts import redirect



class IndexView(View):
    def get(self, request, pk=None):
        posts = Post.objects.select_related("author").all()
        if pk:
            try:
                post = posts.get(id=pk)
                comments = Comment.objects.filter(post=post)
            except (Post.DoesNotExist, Comment.DoesNotExist):
                return redirect('index')
            return render(request, 'details.html', {'post': post, "comments": comments})
        return render(request, 'index.html', {'posts': posts})
class RegisterView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        random_number = random.randint(454545, 686868)

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        user = User(username=username, email=email)
        user.otp = random_number
        send_otp(username, email, random_number)
        user.set_password(password)
        user.save()
        return redirect('verify_otp')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        if check_password(password, user.password):
            request.session['user'] = user.id
            request.session['user_name'] = user.username
            request.session['is_verified'] = user.is_verified
            request.session['is_in'] = True
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class LogoutView(View):
    def get(self, request):
        if request.session.get("is_in"):
            request.session.clear()
            return redirect("index")
        return redirect('login')

class VerifyOTPView(View):
    def get(self, request):
        if request.session.get('is_verified'):
            return redirect('index')
        return render(request, 'verify_otp.html')

    def post(self, request):
        otp = request.POST.get("otp")
        user = User.objects.get(otp=otp)
        user.is_verified = True
        user.save()
        return redirect('login')




class PostCreateView(View):
    def get(self, request):
        return render(request, 'add_post.html')

    def post(self, request):
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        pic = request.FILES.get('pic')
        author_id = request.session['user']
        post = Post(title=title, desc=desc, pic=pic, author=User.objects.get(id=author_id))
        post.save()
        return render(request, 'add_post.html', {'msg': 'Post added successfully'})


class PostUpdateView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author.id != request.session['user']:
            return HttpResponseForbidden()
        return render(request, 'update_post.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author.id != request.session['user']:
            return HttpResponseForbidden()
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        pic = request.FILES.get('pic')
        if pic:
            post.pic = pic
        post.title = title
        post.desc = desc
        post.save()
        return redirect("index")

class PostDeleteView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author.id != request.session['user']:
            return HttpResponseForbidden()
        post.delete()
        return redirect('index')
    


class CommentView(View):
   
    def post(self, request, pk):
        user = User.objects.get(id=request.session['user'])
        post = Post.objects.get(pk=pk)
        comment_text = request.POST.get('comment')
        if user and post and comment_text:
            Comment.objects.create(user=user, post=post, comment=comment_text)
        return redirect('index_with_pk', pk=pk)



class CommentDeleteView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return redirect('index_with_pk', pk=comment.post.id)