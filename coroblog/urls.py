from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('blog.urls'),name='blog'),
    path('admin/', admin.site.urls),
]
