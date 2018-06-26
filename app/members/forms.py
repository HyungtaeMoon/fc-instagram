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
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
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

        print(password)
        print(password2)
        if password != password2:
            self.add_error('password2', '비밀번호와 비밀번호 확인이 다릅니다')
        return self.cleaned_data

    def signup(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password2']
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user