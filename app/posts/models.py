from django.conf import settings
from django.db import models

from members.forms import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='my_comments',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_users',
    )
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

