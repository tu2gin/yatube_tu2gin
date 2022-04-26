import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def check_follow_status(author, user_fol):
    count_fol = Follow.objects.filter(user=user_fol, author=author).count()
    if count_fol == 1:
        return True
    else:
        return False


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAG_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    title = group.title
    description = group.description
    post_list = group.related_name_group.all()
    paginator = Paginator(post_list, settings.PAG_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'description': description,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    if request.user.is_authenticated:
        user_fol = User.objects.get(username=request.user.username)
        follow_status = check_follow_status(author, user_fol)
    else:
        user_fol = ''
        follow_status = False
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, settings.PAG_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': follow_status,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    is_edit = False
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=post.author)
    post_obj = Post.objects.get(id=post_id)
    group = post_obj.group
    pub_date = post_obj.pub_date
    form_comment = CommentForm(request.POST or None,)
    if post.author == request.user:
        is_edit = True
    context = {
        'title': post.text[:30],
        'post': post,
        'pub_date': pub_date,
        'group': group,
        'post_id': post_id,
        'author': author,
        'is_edit': is_edit,
        'form_comment': form_comment,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
@csrf_exempt
def create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(False)
            post.author = request.user
            post.pub_date = datetime.datetime.now()
            post.save()
            return redirect('posts:profile', username=post.author)
    else:
        form = PostForm()

    return render(request, 'posts/create.html', {'form': form})


@login_required
@csrf_exempt
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    is_edit = True
    if request.method == 'POST':
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.datetime.now()
            post.save()
            return redirect('posts:post_detail',
                            post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,
                  'posts/create.html',
                  {'post_id': post_id,
                   'is_edit': is_edit,
                   'form': form,
                   'post': post, })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follow_list = Follow.objects.filter(user=request.user)
    qset = Post.objects.none()
    for list in follow_list:
        qset_temp = Post.objects.filter(author=list.author)
        qset = qset | qset_temp
    paginator = Paginator(qset, settings.PAG_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    user_fol = User.objects.get(username=request.user)
    if author == user_fol:
        post_list = Post.objects.filter(author=author)
        paginator = Paginator(post_list, settings.PAG_POST)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        follow_status = check_follow_status(author, user_fol)
        context = {
            'author': author,
            'page_obj': page_obj,
            'following': follow_status,
        }
        return render(request, 'posts/profile.html', context)

    elif not check_follow_status(author, user_fol):
        post_list = Post.objects.filter(author=author)
        paginator = Paginator(post_list, settings.PAG_POST)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        Follow.objects.create(user=user_fol,
                              author=author,
                              )
        follow_status = check_follow_status(author, user_fol)
        context = {
            'author': author,
            'page_obj': page_obj,
            'following': follow_status,
        }
        return render(request, 'posts/profile.html', context)
    else:
        post_list = Post.objects.filter(author=author)
        paginator = Paginator(post_list, settings.PAG_POST)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        follow_status = check_follow_status(author, user_fol)
        context = {
            'author': author,
            'page_obj': page_obj,
            'following': follow_status,
        }
        return render(request, 'posts/profile.html', context)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    user_fol = User.objects.get(username=request.user)
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, settings.PAG_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    Follow.objects.filter(user=user_fol, author=author).delete()
    follow_status = check_follow_status(author, user_fol)
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': follow_status,
    }
    return render(request, 'posts/profile.html', context)
