from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile
from .forms import PostCreationForm, CommentForm, ProfileCreationForm
from django.views.generic import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate


"""
THE HOME PAGE
"""
def index(request):
    posts = Post.published.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)

# registration

"""
    THE SIGN UP PAGE
"""
def register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])

            print("USER HAS BEEN AUTHENTICATED!!!!")
            login(request, user)

            return redirect('blog:create_profile')

    context = {
        'form': form
    }
    return render(request, 'blog/signup.html', context)

# login_users

"""
    THE LOGIN PAGE
"""
def login_users(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pasword']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect('blog:user_home')
        else:
            messages.add_message(request, messages.INFO, "Invalid Login")

    return render(request, 'blog/login.html', context)

"""
CREATE PROFILE PAGE
"""
@login_required
def create_profile(request):
    form = ProfileCreationForm()

    if request.method == 'POST':
        form=ProfileCreationForm(request.POST,request.FILES)

        if form.is_valid():
            obj=form.save(commit=False)

            obj.user=request.user

            obj.save()

            messages.success(request,"Your account is now set.")

            return redirect("blog:user_home")

    context = {
        'form': form
    }
    return render(request, 'blog/createprofile.html', context)

@login_required
def user_profile(request):
    user_=request.user

    user_profile=Profile.objects.filter(user=user_).first()

    context={
        'profile':user_profile,
        
    }

    return render(request,'blog/profile.html',context)

@login_required
def personal_profile(request,id):
    user_=User.objects.get(id=id)

    profile=Profile.objects.filter(user=user_).first()

    context={
        'profile':profile,
        'user_':user_
    }

    return render(request,'blog/user.html',context)


@login_required 
def post_details(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(post=post).all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.post = post

            obj.author = request.user

            obj.save()

            form = CommentForm()
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/postdetails.html', context)


@login_required
def home_page(request):
    posts = Post.published.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


@login_required
def create_post(request):
    form = PostCreationForm()

    if request.method == "POST":
        form = PostCreationForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.author = request.user

            obj.save()

            messages.success(request, "Post Created Successfully")

            return redirect('blog:user_posts')

    context = {
        'form': form
    }

    return render(request, 'blog/createpost.html', context)


@login_required
def posts(request):
    posts = Post.published.all()

    context = {
        'posts': posts
    }

    return render(request, 'blog/posts.html', context)


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).all()

    context = {
        'posts': posts
    }

    return render(request, 'blog/myposts.html', context)


class PostEditView(UpdateView, SuccessMessageMixin):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/editpost.html'
    success_url = "/posts/"
    success_message = "Post has been Updated successfully"

# @login_required


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/deletepost.html'
    success_url = "/my_posts/"
    context_object_name = 'post'

@login_required
def delete_comment(request, id, slug):
    comment = Comment.objects.get(id=id)
    post = Post.objects.filter(slug=slug).first()

    comment.delete()

    return redirect('/details/{}'.format(post.slug))
