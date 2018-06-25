from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from posts.models import Post


def login_view(request):
    # 1. members.urls <- 'members/'로 include되도록 config.urls모듈에 추가
    # 2. path구현 (URL: '/members/login/')
    # 3. path와 이 view연결
    # 4. 일단 잘 나오는지 확인
    # 5. 잘 나오면 form을 작성(userame, password를 받는 input2개)
    # 6. form작성후에는 POST방식 요청을 보내서 이 뷰에서 request.POST에 요청이 잘 왔는지 확인
    # 7. 일단은 받은 username, password값을 HTTPResponse에 보여주도록 한다

    # return HttpResponse('여기는 login_view 입니다.')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('성공')
            login(request, user)
            return redirect('posts:post-list')

        # 인증에 실패한 경우 (username또는 password가 틀린 경우)
        else:
            # 다시 로그인 페이지로 redirect
            print('실패')
            return redirect('members:login')

    # GET 요청일 경우
    else:
        # form이 있는 template를 보여준다
        return render(request, 'members/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def signup_view(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username:
            context['errors'].append('username을 채워주세요')

        if not email:
            context['errors'].append('email을 채워주세요')

        if not password:
            context['password'].append('password를 채워주세요')

        if not password2:
            context['password2'].append('password2를 채워주세요')

        # 입력데이터 채워넣기
        context['username'] = username
        context['email'] = email

        # form에서 전송된 데이터들이 올바른지 검사
        if User.objects.filter(username=username).exists():
            context['errors'].append('유저가 이미 존재함')
        if password != password2:
            context['errors'].append('패스워드가 일치하지 않음')
            # user = authenticate(request, username=username, password=password2)

        # errors 가 없으면 유저 생성 루틴 실행
        if not context['errors']:
            user = User.objects.create(
                username=username,
                password=password,
                email=email,
            )
            login(request, user)
            return redirect('index')

    return render(request, 'members/signup.html', context)