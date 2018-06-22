from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

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