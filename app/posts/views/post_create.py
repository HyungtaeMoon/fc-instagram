from django.shortcuts import redirect, render

from posts.forms import PostModelForm, PostForm


def post_create(request):
    # PostModelForm을 사용
    #  form = PostModelForm(request.POST, request.FILES)
    #  post = form.save(commit=False)
    #  post.author = request.user
    #  post.save()
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post-detail', pk=post.pk)
    else:
        form = PostModelForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


# @login_required_with_form(login_url='posts:post-list')
def post_create_with_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.post_create(request.user)
            # form에 들어있는 데이터가 유효한지 검사
            # is_valid하면 회원가입 버튼을 누른 상태
            return redirect('index')

    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)
#
# @login_required
# @require_POST
# def post_delete_bak(request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         if post.author != request.user:
#             raise PermissionDenied('지울 권한이 없습니다')
#         post.delete()
#         return redirect('posts:post-list')