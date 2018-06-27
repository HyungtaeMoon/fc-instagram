from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from posts.forms import PostForm
from .models import Post


def post_list(request):
    # return HttpResponse("hello world")
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


@login_required(login_url='posts:post-list')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(form)
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

def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            post.delete()
            return redirect('index')
        else:
            return HttpResponse('권한이 없습니다.')

    return HttpResponse('로그인해주세요')
