from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from posts.forms import PostForm, PostModelForm
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    # PostModelForm을 사용
    #  form = PostModelForm(request.POST, request.FILES)
    #  post = form.save(commit=False)
    #  post.author = request.user
    #  post.save()
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post-detail', pk=post.pk)
    else:
        form = PostModelForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


# @login_required_with_form(login_url='posts:post-list')
def post_create_with_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.post_create(request.user)
            # form에 들어있는 데이터가 유효한지 검사
            # is_valid하면 회원가입 버튼을 누른 상태
            return redirect('index')

    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)
#
# @login_required
# @require_POST
# def post_delete_bak(request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         if post.author != request.user:
#             raise PermissionDenied('지울 권한이 없습니다')
#         post.delete()
#         return redirect('posts:post-list')

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