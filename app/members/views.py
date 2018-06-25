from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import render, redirect

from .forms import SignupForm

# User 클래스 자체를 가져올때는 get_user_model()
# ForeignKey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()


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


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        context = {
            'form': form,
        }
        # form에 들어있는 데이터가 유효한지 검사
        if form.is_valid():
            # 브라우저가 요구하는 형식을 만족
            # 유효할 경우 유저 생성 및 redirect
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            print(form.errors)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            return redirect('index')
        else:

            return render(request, 'members/signup.html', context)

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
#
#
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         # exists를 사용해서 유저가 이미 존재하면 signup으로 다시 redirect
#         if User.objects.filter(username=username).exists():
#             context = {
#                 'errors': [],
#             }
#             context['errors'].append('유저가 이미 존재함')
#             return render(request, 'index', context)
#         else:
#             user = User.objects.create_user(
#                 username=username,
#                 password=password,
#             )
#             login(request, user)
#             return redirect('index')
#     return render(request, 'members/signup.html')
