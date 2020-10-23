from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Post,Comment


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class PostCreationForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','body','status']


class CommentForm(forms.ModelForm):
    body=forms.CharField(
        widget=forms.Textarea(attrs=({'rows':2}))
    )
    class Meta:
        model=Comment
        fields=['body']
