from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..models import Post


@require_POST
@login_required
def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)

        if request.user == post.author:
            post.delete()
            return redirect('index')

        else:
            raise PermissionDenied('지울 권한이 없습니다')

    return HttpResponse('....')
    # post = get_object_or_404(Post, pk=pk)
    # if post.author != request.user:
    #     raise PermissionDenied('지울 권한이 없습니다')
    # else:
    #     post.delete()
    # return redirect('posts:post-list')



# def post_delete(request, pk):
    # if request.method != 'POST':
    #     return HttpResponseNotAllowed()
    # if not request.user.is_authenticated:
    #     return redirect('members:login')