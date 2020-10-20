from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.

#home
def index(request):
    return render(request,'blog/index.html')

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

