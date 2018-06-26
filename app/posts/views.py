from django.http import HttpResponse, HttpResponseRedirect
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

    # return HttpResponse('Post Detail pk: {}'.format(pk))
    post = Post.objects.get(pk=pk)
    context = {
        'post':post,
    }
    return render(request, 'posts/post_detail.html')

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.photo)
        context = {
            'form': form,
        }
        return render(request, 'posts/post_detail.html')
    else:
        return render(request, 'posts/post_create.html')

    # 새 포스트를 만들기
    # 만든 후에는 post_detail로 이동
    # form.py에 PostForm을 구현해서 사용

    # bound form (include file)
    #  PostForm(request.POST)
    #  PostForm(request.POST, request.FILES)

    # POST method에서는 생성후 redirect
    # GET method에서는 form이 보이는 템플릿 렌더링
