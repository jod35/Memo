from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from .forms import PostCreationForm,CommentForm
from django.views.generic import UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate
# Create your views here.

#home
def index(request):
    posts=Post.published.all()
    context={
        'posts':posts
    }
    return render(request,'blog/index.html',context)

#registration
def register(request):
    form=UserRegistrationForm()

    if request.method =="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,"Account Creation Successful, Please Login")

            return redirect('blog:login')

    context={
        'form':form
    }
    return render(request,'blog/signup.html',context)

def login_users(request):
    context={}

    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['pasword']

        user=authenticate(request,username=username,password=password)

        if user is not None:

            login(request,user)

            return redirect('blog:user_home')
        else:
            messages.add_message(request,messages.INFO, "Invalid Login")

    return render(request,'blog/login.html',context)


@login_required
def post_details(request,slug):
    post=Post.objects.filter(slug=slug).first()
    comments=Comment.objects.filter(post=post).all()
    form=CommentForm()


    if request.method == "POST":
        form=CommentForm(request.POST)

        if form.is_valid():
            obj=form.save(commit=False)

            obj.post=post

            obj.author=request.user

            obj.save()

            form=CommentForm()
    else:
        form=CommentForm()

    context={
        'post':post,
        'form':form,
        'comments':comments
    }
    return render(request,'blog/postdetails.html',context)

@login_required
def home_page(request):
    posts=Post.published.all()
    context={
        'posts':posts
    }
    return render(request,'blog/home.html',context)
@login_required
def create_post(request):
    form=PostCreationForm()

    if request.method =="POST":
        form=PostCreationForm(request.POST)

        if form.is_valid():
            obj=form.save(commit=False)

            obj.author=request.user

            obj.save()

            messages.success(request,"Post Created Successfully")

            return redirect('blog:user_posts')

    context={
        'form':form
    }

    return render(request,'blog/createpost.html',context)

@login_required
def posts(request):
    posts=Post.published.all()

    context={
        'posts':posts
    }

    return render(request,'blog/posts.html',context)

@login_required
def my_posts(request):
    posts=Post.objects.filter(author=request.user).all()

    context={
        'posts':posts
    }

    return render(request,'blog/myposts.html',context)

@login_required
class PostEditView(UpdateView,SuccessMessageMixin):
    model=Post
    fields=['title','body']
    template_name='blog/editpost.html'
    success_url="/posts/"
    success_message="Post has been Updated successfully"

@login_required
class PostDeleteView(DeleteView):
    model=Post
    template_name='blog/deletepost.html'
    success_url="/my_posts/"
    context_object_name='post'
