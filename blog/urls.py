from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.register,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='blog/loggedout.html'),name='logout'),
    path('details/<slug>/',views.post_details,name='post_details'),
    path('home/',views.home_page,name='user_home'),
    path('create_post/',views.create_post,name='create_post'),
    path('posts/',views.posts,name='user_posts'),
    path('my_posts',views.my_posts,name='my_posts'),
]