from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .forms import *

# Create your views here.
def test1(request):
    # 서비스 구현
    return HttpResponse('test1!')

def test2(request, id):
    return HttpResponse(id)

def test3(request, year, mon, day):
    return HttpResponse(f'{year}년 {mon}월 {day}일')

def test4(request):
    return render(request, 'blog/test4.html', {'score': 95, 'var': var})



from .models import Post

# def list(request):
#     post_list = Post.objects.all()
#     titles = ""
#     for post in post_list:
#         titles += post.title
#     return HttpResponse(titles)

def detail(request, id):
    post = get_object_or_404(Post, id=id)  # 해당 포스트를 가져오거나 404 에러를 발생시킵니다.
    # return HttpResponse(post.title)
    comment_all = post.comment_set.all()
    tag_list = post.tag.all()
    return render(request, 'blog/detail.html', {'post':post, 'comment_all': comment_all, 'tag_list': tag_list})

def list(request):
    post_list = Post.objects.all()

    search_key = request.Get.get("keyword")
    if search_key:
        post_list = Post.objects.filter(title_contains=search_key)

    return render(request, 'blog/list.html', {'post_all': post_list, 'q':search_key})

def profile(request):
    user = User.objects.get(id=1)
    return render(request, 'blog/profile.html', {'user':user})

def tag_list(request, id):
    tag = Tag.objects.get(id=id)
    post_list = tag.post_set.all()
    return render(request, 'blog/list.html', {'post_list': post_list})

def test7(request):
    print('요청방식 :', request.method)
    print('GET 방식으로 전달된 질의 문자열 :', request.GET)
    print('POST 방식으로 전달된 질의 문자열 :', request.POST)
    print('업로드 파일 :', request.FILES)
    return render(request, 'blog/form_test1.html')


def post_create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # post = Post.objects.create(**form.cleaned_data)
            post = form.save(commit=False)
            post.ip = request.META['REMOTE_ADDR']
            post.save()
            return redirect(Post)
    else:
        form = PostModelForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:list')
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_update.html', {'form': form})

def post_delete(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:list')
    else:
        return render(request, 'blog/post_delete.html', {'post': post})


