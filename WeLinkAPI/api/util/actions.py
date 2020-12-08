# TSH - head
from ..models import Post, Profile, PostComment, PostLike, Friend
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics, filters
from ..serializer import UserSerializer, PostSerializer, ProfileSerializer
# TSH end - head
# ZJN - head

# ZJN end - head

# TSH
# add friends relationship
def add_friends(request):
    f_from = request.GET.get('f_from')
    f_to = request.GET.get('f_to')
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to)
    except Friend.DoesNotExist:
        Friend.objects.update_or_create(friend_from = f_from, friend_to = f_to)
# TODO: get all posts that you are allowed to see

# TODO: get all posts for a certain user that you can see

# TSH end
# ZJN

# ZJN end