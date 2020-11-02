from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile
from .forms import PostCreationForm, CommentForm, ProfileCreationForm
from django.views.generic import UpdateView, DeleteView,ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate
from django.views import View
from django.core.paginator import Paginator


"""
THE HOME PAGE
"""

class IndexPageview(ListView):
    template_name='blog/index.html'
    model=Post
    queryset=Post.objects.all()
    paginate_by=5


"""
    THE SIGN UP PAGE
"""


class SignUpView(View):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'blog/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1']
                                )

            login(request, user)

            return redirect('blog:create_profile')

        return render(request, self.template_name, {'form': form})


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
        form = ProfileCreationForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.user = request.user

            obj.save()

            messages.success(request, "Your account is now set.")

            return redirect("blog:user_home")

    context = {
        'form': form
    }
    return render(request, 'blog/createprofile.html', context)


class CurrentUserProfile(View):
    template_name='blog/profile.html'

    def get(self,request,*args,**kwargs):
        user_profile=Profile.objects.filter(user=request.user).first()
        posts=Post.objects.filter(author=request.user).all()

        paginator=Paginator(posts,5)

        page_number=request.GET.get('page')

        page_obj=paginator.get_page(page_number)

        return render(request,self.template_name,({'profile':user_profile,
            'page_obj':page_obj
        }))



class PersonalProfileView(View):
    template_name='blog/user.html'

    def get(self,request,id,*args,**kwargs):
        user_ = User.objects.get(id=id)

        profile = Profile.objects.filter(user=user_).first()

        posts = Post.objects.filter(author=user_).all()

        paginator=Paginator(posts,5)

        page_number=request.GET.get('page')

        page_obj=paginator.get_page(page_number)

        context = {
            'profile': profile,
            'user_': user_,
            'page_obj': page_obj
        }

        return render(request, 'blog/user.html', context)




class PostDetailView(View):
    
    form_class=CommentForm
    initial={'key':'value'}
    template_name='blog/postdetails.html'

    def get(self,request,slug,*args,**kwargs):
        post = Post.objects.filter(slug=slug).first()
        comments = Comment.objects.filter(post=post).all()
        form=self.form_class(initial=self.initial)

        context={
            'comments':comments,
            'form':form,
            'post':post
        }

        return render(request,self.template_name,context)

    def post(self,request,slug,*args,**kwargs):
        form=self.form_class(request.POST)
        post = Post.objects.filter(slug=slug).first()

        comments = Comment.objects.filter(post=post).all()
        if form.is_valid():
            obj = form.save(commit=False)

            obj.post = post

            obj.author = request.user

            obj.save()

        context={'post':post,'form':form,'comments':comments}

        return render(request,self.template_name,context)


class HomePageView(View):
    template_name='blog/home.html'
    query_set=Post.published.all()

    def get(self,request,*args,**kwargs):
        paginator=Paginator(self.query_set,5)

        page_number=request.GET.get('page')

        page_obj=paginator.get_page(page_number)

        return render(request,self.template_name,{'page_obj':page_obj})
        
    

class CreatePostView(View):
    template_name='blog/createpost.html'
    form_class=PostCreationForm
    initial={'key':'value'}

    def get(self,request,*args,**kwargs):
        form=self.form_class(initial=self.initial)

        return render(request,self.template_name,{'form':form})

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)

        if form.is_valid():
            obj=form.save(commit=False)
            obj.author=request.user

            obj.save()

            messages.success(request,"Post Created Successfully")

            return redirect('blog:user_posts')

        return render(request,self.template_name,{'form':form})

            


@login_required
def posts(request):
    posts = Post.published.all()

    paginator=Paginator(posts,5)

    page_number=request.GET.get('page')

    page_obj=paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'blog/posts.html', context)


class MyPostView(View):
    template_name='blog/myposts.html'
    def get(self,request,*args,**kwargs):
        posts=Post.objects.filter(author=request.user).all()

        paginator=Paginator(posts,5)

        page_number=request.GET.get('page')

        page_obj=paginator.get_page(page_number)

        return render(request,self.template_name,{'page_obj':page_obj})
    



class PostEditView(UpdateView, SuccessMessageMixin):
    model = Post
    fields = ['title', 'body','status']
    template_name = 'blog/editpost.html'
    success_url = "/posts/"
    success_message = "Post has been Updated successfully"
    context_object_name = 'post/editpost.html'

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


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'blog/editprofile.html'
    context_object_name = ''
