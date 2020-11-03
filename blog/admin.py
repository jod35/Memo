from django.contrib import admin
from .models import Post,Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['author','body','created','publish',]
    prepopulated_fields={'slug':('body',)}
    list_filter=['created','publish',]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user']
    
