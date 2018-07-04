from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from posts.models import Post, Comment


@login_required
@require_POST
def comment_create(request, post_pk, comment_pk=None):
    post = get_object_or_404(Post, pk=post_pk)
    if comment_pk:
        parent_comment = get_object_or_404(Comment, comment_pk)
    else:
        parent_comment = None
    parent_comment = get_object_or_404(Comment, pk=comment_pk if comment_pk else None)
    post.comments.create(
        author=request.user,
        content=request.POST.get('content'),
        parent_comment=parent_comment,
    )
    return redirect('posts:post-detail', post_pk)