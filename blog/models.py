from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pics', default='default.png')
    bio = models.TextField()

    def __str__(self):
        return f"{self.user}"




class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')


    slug = models.SlugField(
        max_length=250, unique_for_date='publish', db_index=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-publish']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.body)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post'
    )

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='authors'
                               )

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body} by {self.author}"

    ordering = ('created',)


class Follower(models.Model):
    user=models.ManyToManyField(User)