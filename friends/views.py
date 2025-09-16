from django.shortcuts import render
from .models import FriendRequest
from django.contrib.auth.decorators import login_required

@login_required
def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'friends/friend_requests.html', {'requests': requests})
