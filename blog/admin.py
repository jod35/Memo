from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','created','publish',]
    prepopulated_fields={'slug':('title',)}
    list_filter=['created','publish',]
    