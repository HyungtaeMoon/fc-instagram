from django import forms
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


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
