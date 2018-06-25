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
        reputation = self.cleaned_data['username']

        if User.objects.filter(username=reputation):
            raise ValidationError('무조건 에러')

        return reputation

    def clean_password(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise ValidationError('에러가 났습니다')
