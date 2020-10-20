from django.shortcuts import render
from .forms import UserRegistrationForm

# Create your views here.

#home
def index(request):
    return render(request,'blog/index.html')

#registration
def register(request):
    form=UserRegistrationForm()
    context={
        'form':form
    }
    return render(request,'blog/signup.html',context)

