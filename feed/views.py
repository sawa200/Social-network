from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # обязательно добавить request.FILES!
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'feed/create_post.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(f"/#post-{post.id}")



