from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from .signals import create_profile,save_user_profile
from .models import User


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        import blog.signals
