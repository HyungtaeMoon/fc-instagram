from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostForm, PostModelForm
from .models import Post


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
#
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied('지울 권한이 없습니다')
    post.delete()
    return redirect('posts:post-list')

    # if request.method == 'POST':
    #     post = Post.objects.get(pk=pk)
    #     if post.author == request.user:
    #         post.delete()
    #         return HttpResponse('권한이 없습니다')
    #     else:
    #         return render(request, 'posts/403.html')
    #
    # return HttpResponse('로그인해주세요')


# def post_delete(request, pk):
#     if request.method != 'POST':
#         return HttpResponseNotAllowed()
#     if not request.user.is_authenticated:
#         return redirect('members:login')