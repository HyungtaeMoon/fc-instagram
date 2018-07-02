from django.conf import settings
from django.db import models

from members.forms import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        # 1. related_name은 반대쪽(target)에서 이쪽(source)로의 연결을 만들어주는 Mannager
        # 2. 자신이 like_users에 포함이 되는 Post QUerySet Manager
        # 3. -> 내가 좋아요 누른 Post목록,
        related_name='like_posts',
    )

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

