from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [
    path('', login_required(views.IndexPageview.as_view()), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/loggedout.html'), name='logout'),
    path('details/<slug>/', login_required(views.PostDetailView.as_view()),
         name='post_details'),
    path('home/', login_required(views.HomePageView.as_view()), name='user_home'),
    path('create_post/', login_required(views.CreatePostView.as_view()),
         name='create_post'),
    path('posts/', login_required(views.PostView.as_view()), name='user_posts'),
    path('my_posts/', login_required(views.MyPostView.as_view()), name='my_posts'),
    path('edit_post/<slug>',
         login_required(views.PostEditView.as_view()), name='edit_post'),
    path('delete_post/<pk>',
         login_required(views.PostDeleteView.as_view()), name='delete_post'),
    path('create_profile/', login_required(views.ProfileCreationView.as_view()),
         name='create_profile'),
    path('delete_comment/<int:id>/<slug>',
         login_required(views.CommentDeleteView.as_view()), name='delete_comment'),
    path('profile/', login_required(views.CurrentUserProfile.as_view()),
         name='user_profile'),
    path('profile/<int:id>/',
         login_required(views.PersonalProfileView.as_view()), name='user_profile'),
    path('edit_profile/profile<pk>/',
         login_required(views.ProfileEditView.as_view()), name='edit_profile'),
]
