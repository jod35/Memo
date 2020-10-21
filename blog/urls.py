from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='blog'

urlpatterns = [
    path('',views.index,name='home'),
    path('signup/',views.register,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='blog/loggedout.html'),name='logout'),
    path('details/<slug>/',views.post_details,name='post_details'),
]