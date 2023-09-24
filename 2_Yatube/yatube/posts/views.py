from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import get_page


def index(request):
    post_list = Post.objects.select_related('group', 'author')
    page_obj = get_page(request, post_list)
    return render(
        request,
        "posts/index.html",
        {"page_obj": page_obj},
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author')
    page_obj = get_page(request, post_list)
    return render(
        request,
        "posts/group_list.html",
        {"group": group, "page_obj": page_obj},
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group')
    page_obj = get_page(request, post_list)
    following = author.is_authenticated and (
        request.user != author) and Follow.objects.filter().exists()
    return render(
        request,
        "posts/profile.html",
        {"author": author, "page_obj": page_obj, "following": following},
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post).select_related('author')
    return render(
        request,
        "posts/post_detail.html",
        {"post": post, "form": form, "comments": comments},
    )


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:profile", request.user.username)
        return render(request, "posts/create_post.html", {"form": form})
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect("posts:post_detail", post_id=post.id)
    if request.method == "POST":
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", post_id=post.id)
    form = PostForm(instance=post)
    return render(
        request,
        "posts/create_post.html",
        {"form": form, "is_edit": True, "post_id": post_id})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follower = Follow.objects.filter(
        user=request.user).values_list(
        "author_id", flat=True
    )
    posts = Post.objects.filter(author_id__in=follower)
    page_obj = get_page(request, posts)
    return render(
        request,
        "posts/follow.html",
        {"page_obj": page_obj}
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("posts:follow_index")


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("posts:follow_index")
