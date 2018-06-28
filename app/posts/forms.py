from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from posts.models import Post

User = get_user_model()



class PostModelForm(forms.ModelForm):
    # field정의를 직접 하지 않음
    # (어떤 field를 사용할 것이지만 class Meta에 기록)
    class Meta:
        model = Post
        fields = ('author',
                  'photo',
                  'content'
                  )


class PostForm(forms.Form):
    content = forms.CharField(
        label='글 작성하기',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'style': 'resize: none'
            }
        )
    )
    file = forms.ImageField(
        label='사진 올리기',
    )

    def post_create(self, user):
        content = self.cleaned_data['content']
        photo = self.cleaned_data['file']
        Post.objects.create(
            author=user,
            content=content,
            photo=photo,
        )
