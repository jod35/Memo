from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.register,name='signup'),
    path('login/',views.login_users,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='blog/loggedout.html'),name='logout'),
    path('details/<slug>/',views.post_details,name='post_details'),
    path('home/',views.home_page,name='user_home'),
    path('create_post/',views.create_post,name='create_post'),
    path('posts/',views.posts,name='user_posts'),
    path('my_posts/',views.my_posts,name='my_posts'),
    path('edit_post/<slug>',views.PostEditView.as_view(),name='edit_post'),
    path('delete_post/<pk>',views.PostDeleteView.as_view(),name='delete_post'),
    path('create_profile/',views.create_profile,name='create_profile'),
    path('delete_comment/<int:id>/<slug>',views.delete_comment,name='delete_comment'),
    path('profile/',views.user_profile,name='user_profile'),
    path('profile/<int:id>/',views.personal_profile,name='user_profile')
]
