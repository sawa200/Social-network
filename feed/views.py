from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment
from .forms import CommentForm, PostForm
from users.models import Friendship 

def index(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "feed/index.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by("-created_at")  

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("feed:post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "feed/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
    })


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("feed:index")
    else:
        form = PostForm()
    return render(request, "feed/create_post.html", {"form": form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": post.likes.count()
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("feed:post_detail", post_id=post.id)


@login_required
def friends_feed(request):
  
    friends_from = Friendship.objects.filter(from_user=request.user).values_list("to_user_id", flat=True)
    friends_to = Friendship.objects.filter(to_user=request.user).values_list("from_user_id", flat=True)


    friends_ids = list(friends_from) + list(friends_to)

   
    posts = Post.objects.filter(author__id__in=friends_ids).order_by("-created_at")

    return render(request, "feed/friends_feed.html", {"posts": posts})
