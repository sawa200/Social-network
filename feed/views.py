from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(author=request.user, title=title, content=content)
            return redirect('index')
    return render(request, 'feed/create_post.html')
