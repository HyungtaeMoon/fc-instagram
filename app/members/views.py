import json

import requests
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config import settings
from .forms import SignupForm

# User 클래스 자체를 가져올때는 get_user_model()
# ForeignKey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts:post-list')
        else:
            return redirect('members:login')

    else:
        return redirect(request, 'members/login.html')


def login_view(request):

    # 1. POST요청이 왔는데, 요청이 올바르면서
    # 2. GET parameter에 'next'값이 존재할 경우
    # 3. 해당 값(URL)로 redirect
    # 4. next값이 존재하지 않으면 원래 이동하던 곳으로 그대로 redirect

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
            # 세션값을 만들어 DB에 저장하고, HTTP response의 Cookie에 해당값을 담아보내도록 하는
            # login()함수를 실행한다

            # session)id값을 django_sessions테이블에 저장, 데이터는 user와 연결됨
            # 이 함수 실행 후 돌려줄 HTTP Response에는 Set-Cookie헤더를 추가, 내용은 session=<session값>
            login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
                # print(request.GET.get('next'))
            return redirect('posts:post-list')

        # 인증에 실패한 경우 (username또는 password가 틀린 경우)
        else:
            # 다시 로그인 페이지로 redirect
            return redirect('members:login')

    # GET 요청일 경우
    else:
        # form이 있는 template를 보여준다
        return render(request, 'members/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        context = {
            'form': form,
        }
        # form에 들어있는 데이터가 유효한지 검사
        # is_valid하면 회원가입 버튼을 누른 상태
        if form.is_valid():
            user = form.signup()
            login(request, user)
            return redirect('index')

    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        # if request.method == 'POST':
    return render(request, 'members/signup.html', context)


def signup_bak(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # 반드시 내용이 채워져야 하는 form의 필드 (위 변수명)
        # hint: required_fields를 dict로
        require_fields = {
            'username': {
                'verbose_name': '아이디',
            },
            'email': {
                'verbose_name': '이메일',
            },
            'password': {
                'verbose_name': '비밀번호',
            },
            'password2': {
                'verbose_name': '비밀번호 확인',
            },
        }
        for field_name in require_fields.keys():
            if not locals()[field_name]:
                context['errors'].append('{}을(를) 채워주세요.'.format(
                    require_fields[field_name]['verbose_name'],
                ))

        # for문으로 작동하도록 수정
        # if not username:
        #     context['errors'].append('username을 채워주세요')
        #
        # if not email:
        #     context['errors'].append('email을 채워주세요')
        #
        # if not password:
        #     context['password'].append('password를 채워주세요')
        #
        # if not password2:
        #     context['password2'].append('password2를 채워주세요')

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


@login_required(login_url='posts:post-list')
def withdraw(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')
#
# def signup(request):
#     context = {
#         'errors': [],
#     }
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#
#         # 입력데이터 채워넣기
#         context['username'] = username
#         context['email'] = email
#
#         # form에서 전송된 데이터들이 올바른지 검사
#         if User.objects.filter(username=username).exists():
#             context['errors'].append('유저가 이미 존재함')
#         if password != password2:
#             context['errors'].append('비밀번호가 다릅니다')
#
#         if not context['errors']:
#             user = User.objects.create_user(
#                 username=username,
#                 password=password,
#             )
#             login(request, user)
#             return redirect('index')
#     return render(request, 'members/signup.html', context)


def follow_toggle(request):
    if request.method == 'POST':
        follow = User(

        )
        pass

def facebook_login(request):
    # GET parameter의 'code'에 값이 전달됨 (authentication code)
    # 전달받은 인증코드를 사용해서 액세스 토큰을 받음
    code = request.GET.get('code')
    url = 'https://graph.facebook.com/v3.0/oauth/access_token'
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET_CODE,
        'code': code,
    }
    response = requests.get(url, params)
    # 파이썬에 내장된 json모듈을 사용해서, JSON 형식의 텍스트를 파이썬 Object로 변환
    response_dict = json.loads(response.text)

    # 위와 같은 결과
    response_dict = response.json()
    access_token = response_dict['access_token']

    # debug_token에 요청 보내고 결과 받기
    # 받은 결과의 'data'값을 HttpResponse로 출력
    # input_token은 위의 'access_token'
    # access_token은 {client_id}|{client_secret}값

    url = 'https://graph.facebook.com/debug_token'
    params = {
        'input_token': access_token,
        'access_token': '{}|{}'.format(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET_CODE,
        )
    }


    # GraphAPI를 'me'(user)이용해서 Facebook User정보 받아오기
    url = 'https://graph.facebook.com/v3.0/me'
    params = {
        'fields': ','.join([
            'id',
            'name',
            'first_name',
            'last_name',
            'picture'
        ]),
        # 'fields': 'id,name,first_name,last_name,picture',
        'access_token': access_token,
    }
    response = requests.get(url, params)
    response_dict = response.json()

    # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
    facebook_user_id = response_dict['id']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_img_profile = response_dict['picture']['data']['url']

    user, user_created = User.objects.get_or_create(
        username=facebook_user_id,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
        }

    )
    # 유저가 새로 생성되었다면
    # if user_created:
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
    login(request, user)
    return redirect('index')

    # 왼쪽 액세스 코드 교환 엔드포인트에 HTTP GET요청 후,
    # 결과 response.text값을 HttpResponse에 출력
