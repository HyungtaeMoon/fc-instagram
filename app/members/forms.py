from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        label='이메일 주소',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        required=False,
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    introduce = forms.CharField(
        required=False,
        label='소개하기',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
            )
        )

    site = forms.CharField(
        label='사이트',
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    gender = forms.ChoiceField(
        label='성별',
        choices=(
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택안함'),
        ),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    img_profile = forms.ImageField(
        required=False,
        label='프로필 사진',
    )

    def clean_username(self):
        # field의 clean()실행 결과가 self.cleaned_data['username']에 있음
        data = self.cleaned_data['username']

        if User.objects.filter(username=data).exists():
            raise ValidationError('이미 사용중인 아이디입니다')
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            self.add_error('password2', '비밀번호와 비밀번호 확인이 다릅니다')
        return self.cleaned_data

    def signup(self):
        fields = [
            'username',
            'email',
            'password',
            'img_profile',
            'introduce',
            'gender',
            'site',
        ]
        create_user_dict = {}
        for key, value in self.cleaned_data.items():
            if key in fields:
                create_user_dict[key] = value

        create_user_dict = {key: value for key, value in self.cleaned_data.items() if key in fields}

        # filter를 사용
        def in_fields(item):
            return item[0] in fields

        result = filter(in_fields, self.cleaned_data.items())
        for item in result:
            create_user_dict[item[0]] = item[1]

        # filter결과를 dict함수로 묶어서 새 dict생성
        create_user_dict = dict(filter(in_fields, self.cleaned_data.items()))
        create_user_dict = dict(filter(lambda item: item[0] in fields, self.cleaned_data.items()))

        user = User.objects.create_user(**self.cleaned_data)
        # username = self.cleaned_data['username']
        # email = self.cleaned_data['email']
        # password = self.cleaned_data['password2']
        # img_profile = self.cleaned_data['img_profile']
        # introduce = self.cleaned_data['introduce']
        # gender = self.cleaned_data['gender']
        # site = self.cleaned_data['site']
        # user = User.objects.create_user(
        #     username=username,
        #     email=email,
        #     password=password,
        #     img_profile=img_profile,
        #     introduce=introduce,
        #     gender=gender,
        #     site=site,
        # )
        return user
