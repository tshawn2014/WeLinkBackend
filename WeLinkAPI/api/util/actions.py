# TSH - head
from ..models import Post, Profile, PostComment, PostLike, Friend, Tag, PostTag
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics, filters
from ..serializer import ProfileSerializer, PostSerializer
from django.contrib.auth.models import User as AuthUser
import json
from django.core import serializers
from rest_framework.renderers import JSONRenderer
# TSH end - head
# ZJN - head

# ZJN end - head

# TSH
# add friends relationship
def add_friends(request):
    f_from = request.user
    f_to_id = request.GET.get('f_to')
    try:
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        return HttpResponse('not OK')
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to)
    except Friend.DoesNotExist:
        t, _ = Tag.objects.get_or_create(user=f_from, tag_info='default')
        Friend.objects.update_or_create(friend_from = f_from, friend_to = f_to, tag = t)
    return HttpResponse('OK')

def delete_friends(request):
    f_from = request.user
    f_to_id = request.GET.get('f_to')
    try:
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        return None
    try:
        f = Friend.objects.filter(friend_from = f_from, friend_to = f_to)
        f.delete()
    except Friend.DoesNotExist:
        pass
    return HttpResponse('OK')
        

# add friends tag
def add_tag(request):
    f_from = request.user
    f_to_id = request.GET.get('f_to')
    tag = request.GET.get('tag', '')
    try:
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        return HttpResponse('not OK')

    t, _ = Tag.objects.get_or_create(user = f_from, tag_info = tag) 
    
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to, tag=t)
    except Friend.DoesNotExist:
        Friend.objects.update_or_create(friend_from = f_from, friend_to = f_to, tag=t)
    return HttpResponse('OK')

def remove_tag(request):
    f_from = request.user
    f_to_id = request.GET.get('f_to')
    tag = request.GET.get('tag', '')
    if tag == '':
        return HttpResponse("not OK") 
    try:
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        return HttpResponse('not OK')
    t, _ = Tag.objects.get_or_create(user = f_from, tag_info = tag) 
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to, tag=t)
        f.delete()
    except Friend.DoesNotExist:
        pass
    return HttpResponse("OK")

# get all users relationship
def get_friends(request):
    f_from = request.user
    try:
        f = Friend.objects.filter(friend_from = f_from).values("friend_from", "friend_to", "tag__tag_info", "tag__id")
    except Friend.DoesNotExist:
        pass
    res = {}
    for fields in f:
        t = int(fields['friend_to'])
        f_to = AuthUser.objects.get(id=t)
        friend = Profile.objects.filter(user=f_to).values("name", "email")[0]
        if t not in res.keys():
            res[t] = {
                "friend_to": {
                    "id":t,
                    "name":friend["name"],
                    "email":friend["email"]
                },
                "tags": [
                    {"info":fields['tag__tag_info'], "tag_id":fields['tag__id']}
                ]
            }
        else:
            res[t]["tags"].append({"info":fields['tag__tag_info'], "tag_id":fields['tag__id']})
    res = [x for x in res.values()]
    return HttpResponse(json.dumps(res))

# get all posts that you are allowed to see
def get_visible_posts(request):
    user = request.user
    # get all tags
    tags = Friend.objects.filter(friend_to=user).select_related('tag')
    print(tags)
    # get all posts
    res = None
    for t in tags:
        if res == None:
            res = PostTag.objects.filter(tag=t.tag).select_related("post")
        else:
            p = PostTag.objects.filter(tag=t.tag).select_related("post")
            res.union(p)
    ids = [int(x["post__id"]) for x in res.values("post__id")]
    print(ids)
    q = Post.objects.filter(id__in=ids).order_by("-create_time")
    print("xxx",q)
    res = [PostSerializer(x).data for x in q]
    # json = JSONRenderer().render(res.data)
    js = json.dumps(res)
    return HttpResponse(js)
    


# TODO: get all posts for a certain user that you can see
def get_visible_posts_of_one(request):
    user = request.user
    f_to_id = request.GET.get('f_to')
    try:
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        return HttpResponse('not OK')
    # get all tags
    tags = Friend.objects.filter(friend_to=user, friend_from=f_to).select_related('tag')
    print(tags)
    # get all posts
    res = None
    for t in tags:
        if res == None:
            res = PostTag.objects.filter(tag=t.tag).select_related("post")
        else:
            p = PostTag.objects.filter(tag=t.tag).select_related("post")
            res.union(p)
    ids = [int(x["post__id"]) for x in res.values("post__id")]
    print(ids)
    q = Post.objects.filter(id__in=ids).order_by("-create_time")
    print("xxx",q)
    res = [PostSerializer(x).data for x in q]
    # json = JSONRenderer().render(res.data)
    js = json.dumps(res)
    return HttpResponse(js)
# TSH end
# ZJN

# ZJN end