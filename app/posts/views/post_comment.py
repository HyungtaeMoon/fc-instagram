from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..models import Post, Comment


@login_required
def comment_create(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        Comment.objects.create(
            post=post,
            user=request.user,
            content=request.POST.get('comment'),
        )
        return redirect('posts:post-detail', post.pk)
    return render(request, 'posts:post-detail')
