from django.http import HttpResponse
from django.shortcuts import render

# post_list(request)
# post_detail(request, pk) <- view parameter 및 path패턴명에 'pk'사용

# 구현하세요
# base.html기준으로
# TEMPLATE설정 쓸 것 (teemplates폴더를 DIR에 추가)
#     -> 경로이름은 TEMPLATES_DIR로 settings.py의 윗부분에 추가

# post_list는 'posts/post_list.html'
# post_detail은 'posts/post_detail.html' 사용

# 1. view와 url의 연결 구현
# 2. view에서 template을 렌더링하는 기능 추가
# 3. template에서 QuerySet또는 object를 사용해서 객체 출력
# 4. template에 extend 사용

from .models import Post

def post_list(request):
    return HttpResponse("hello world")
    # # posts = Post.objects.order_by('-id')
    # context = {
    #     'posts': posts,
    # }
    # return render(
    #     request, 'posts/post_list.html', context
    # )

def post_detail(requet, pk):
    return HttpResponse('Post Detail pk: {}'.format(pk))