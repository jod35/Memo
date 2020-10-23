from django.contrib import admin
from .models import Post,Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','created','publish',]
    prepopulated_fields={'slug':('title',)}
    list_filter=['created','publish',]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user']
    
