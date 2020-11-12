from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Post, Comment, Profile, Follower
from .forms import PostCreationForm, CommentForm, ProfileCreationForm,PostEditForm
from django.views.generic import UpdateView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate
from django.views import View
from django.core.paginator import Paginator


"""
THE HOME PAGE
"""


class IndexPageview(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = Post.objects.all()
    paginate_by = 5


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


class LoginPageView(View):
    template_name = 'blog/login.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['pasword']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect('blog:user_home')
        else:
            messages.add_message(request, messages.INFO, "Invalid Login")

        return render(request, self.template_name)


"""
CREATE PROFILE PAGE
"""


class ProfileCreationView(View):
    template_name = 'blog/createprofile.html'
    form_class = ProfileCreationForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProfileCreationForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.user = request.user

            obj.save()

            messages.success(request, "Your account is now set.")

            return redirect("blog:user_home")
        return render(request, self.template_name, {'form': form})


"""
    PROFILE VIEW FOR CURRENTLY LOGGED IN USER
"""


class CurrentUserProfile(View):
    template_name = 'blog/profile.html'

    def get(self, request, *args, **kwargs):
        user_profile = Profile.objects.filter(user=request.user).first()
        posts = Post.objects.filter(author=request.user).all()

        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, ({'profile': user_profile,
                                                     'page_obj': page_obj
                                                     }))


"""
PROFILE VIEW FOR OTHER USERS
"""


class PersonalProfileView(View):
    template_name = 'blog/user.html'

    def get(self, request, username, *args, **kwargs):
        user_ = User.objects.filter(username=username).first()

        profile = Profile.objects.filter(user=user_).first()

        posts = Post.objects.filter(author=user_).all()

        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {
            'profile': profile,
            'user_': user_,
            'page_obj': page_obj
        }

        return render(request, 'blog/user.html', context)

        def post(self, request, id, *args, **kwargs):

            user = get_object_or_404(User, id=id)

            # new_follower=Follower(user=)


"""
    POST DETAIL VIEW
"""


class PostDetailView(View):

    form_class = CommentForm
    initial = {'key': 'value'}
    template_name = 'blog/postdetails.html'

    def get(self, request, slug, *args, **kwargs):
        post = Post.objects.filter(slug=slug).first()
        comments = Comment.objects.filter(post=post).all()
        form = self.form_class(initial=self.initial)

        context = {
            'comments': comments,
            'form': form,
            'post': post
        }

        return render(request, self.template_name, context)

    def post(self, request, slug, *args, **kwargs):
        form = self.form_class(request.POST)
        post = Post.objects.filter(slug=slug).first()

        comments = Comment.objects.filter(post=post).all()
        if form.is_valid():
            obj = form.save(commit=False)

            obj.post = post

            obj.author = request.user

            obj.save()

            form = self.form_class(initial=self.initial)

        context = {'post': post, 'form': form, 'comments': comments}

        return render(request, self.template_name, context)


"""
    HOME PAGE VIEW
"""


class HomePageView(View):
    template_name = 'blog/home.html'
    query_set = Post.objects.all()

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.query_set, 5)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj})


"""
    VIEW FOR CREATION OF POSTS
"""


class CreatePostView(View):
    template_name = 'blog/createpost.html'
    form_class = PostCreationForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user

            obj.save()

            messages.success(request, "Post Created Successfully")

            return redirect('blog:user_posts')

        return render(request, self.template_name, {'form': form})


"""
    A LIST VIEW FOR POSTS
"""


class PostView(ListView):
    model = Post
    queryset = Post.objects.all()
    paginate_by = 5
    template_name = 'blog/posts.html'


"""
    VIEW FOR LIKING POSTS
"""


@require_POST
@login_required
def like_post(request, id):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)

            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)

            return redirect('blog:user_home')

        except:
            pass

    return redirect('blog:user_home')


"""
 VIEW FOR POSTS BY THE CURRENT USER
"""


class MyPostView(View):
    template_name = 'blog/myposts.html'

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(author=request.user).all()

        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj})


"""
VIEW FOR DELETION OF POSTS
"""


class PostEditView(UpdateView, SuccessMessageMixin):
    model = Post
    template_name = 'blog/editpost.html'
    success_url = "/posts/"
    success_message = "Post has been Updated successfully"
    context_object_name = 'post/editpost.html'
    form_class=PostEditForm
    


"""
    view for deleting posts
"""


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/deletepost.html'
    success_url = "/my_posts/"
    context_object_name = 'post'


"""
    view for deleting comments
"""


class CommentDeleteView(View):
    def get(self, request, id, slug, *args, **kwargs):

        comment = Comment.objects.get(id=id)
        post = Post.objects.filter(slug=slug).first()

        comment.delete()

        return redirect('/details/{}/'.format(post.slug))


"""View for editing a user profile"""


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'blog/editprofile.html'
    context_object_name = 'profile'
    fields = ['profile_pic', 'bio']
    success_url = '/profile/'
