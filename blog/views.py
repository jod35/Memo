from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post

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

