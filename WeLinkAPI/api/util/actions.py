# TSH - head
from ..models import Post, Profile, PostComment, PostLike, Friend, Tag, PostTag
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics, filters
from ..serializer import ProfileSerializer, PostSerializer, TagSerializer
from django.contrib.auth.models import User as AuthUser
import json
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from re import sub
# from rest_framework.authtoken.models import Token
# from django.core.models import OrganizationRole, Organization, User
# TSH end - head
# ZJN - head

# ZJN end - head

# TSH
# def get_user(request):
#     header_token = request.META.get('HTTP_AUTHORIZATION', None)
#     print(header_token)
#     if header_token is not None:
#       try:
#         token = sub('Token ', '', request.META.get('HTTP_AUTHORIZATION', None))
#         token_obj = Token.objects.get(key = token)
#         request.user = token_obj.user
#       except Token.DoesNotExist:
#         pass
#     #This is now the correct user
#     return request.user

# add friends relationship
def add_friends(request):
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    f_to_id = int(request.GET.get('f_to'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from id in db")
        return HttpResponse('not OK')
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to)
    except Friend.DoesNotExist:
        t, _ = Tag.objects.get_or_create(user=f_from, tag_info='default')
        Friend.objects.update_or_create(friend_from = f_from, friend_to = f_to, tag = t)
    return HttpResponse('OK')

def delete_friends(request):
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    f_to_id = int(request.GET.get('f_to'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from or f_to id in db")
        return HttpResponse('not OK')
    try:
        f = Friend.objects.filter(friend_from = f_from, friend_to = f_to)
        f.delete()
    except Friend.DoesNotExist:
        pass
    return HttpResponse('OK')
        

# add friends tag
def add_tag(request):
    tag = request.GET.get('tag', '')
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    f_to_id = int(request.GET.get('f_to'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from or f_to id in db")
        return HttpResponse('not OK')

    t, _ = Tag.objects.get_or_create(user = f_from, tag_info = tag) 
    
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to, tag=t)
    except Friend.DoesNotExist:
        Friend.objects.update_or_create(friend_from = f_from, friend_to = f_to, tag=t)
    return HttpResponse('OK')

def remove_tag(request):
    tag = request.GET.get('tag', '')
    if tag == '':
        print("tag cannot be empty")
        return HttpResponse("not OK") 
    f_from_id = int(request.GET.get('f_from'))
    f_to_id = int(request.GET.get('f_to'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from or f_to id in db")
        return HttpResponse('not OK')
    t, _ = Tag.objects.get_or_create(user = f_from, tag_info = tag) 
    try:
        f = Friend.objects.get(friend_from = f_from, friend_to = f_to, tag=t)
        f.delete()
    except Friend.DoesNotExist:
        pass
    return HttpResponse("OK")

# get all users with following or not
def get_friends(request):
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    f_to_id = int(request.GET.get('f_to'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from or f_to id in db")
        return HttpResponse('not OK')
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
    res = {
        "success":True,
        "data":res
    }
    return HttpResponse(json.dumps(res))

# get all users with following or not
def get_friends(request):
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    # f_to_id = int(request.GET.get('f_to'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        # f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from id in db")
        return HttpResponse('not OK, no user')
    try:
        f = Friend.objects.filter(friend_from = f_from).values("friend_from", "friend_to", "tag__tag_info", "tag__id")
    except Friend.DoesNotExist:
        pass
    res = {}
    for fields in f:
        t = int(fields['friend_to'])
        f_to = AuthUser.objects.get(id=t)
        friend = Profile.objects.filter(user=f_to).values("name", "email", "avatar")[0]
        if t not in res.keys():
            res[t] = {
                "id":t,
                "name":friend["name"],
                "email":friend["email"],
                "imgUrl": friend["avatar"],
                "following":True,
                "input": "",
                "tags": [
                    {"content":fields['tag__tag_info'], "id":fields['tag__id']}
                ]
            }
        else:
            res[t]["tags"].append({"content":fields['tag__tag_info'], "id":fields['tag__id']})
    all_user = Profile.objects.all().values("user__id", "name", "email", "avatar")
    for u in all_user:
        uid = int(u["user__id"])
        if uid not in res.keys():
            res[uid] = {
                "id":uid,
                "name":u["name"],
                "email":u["email"],
                "imgUrl": u["avatar"],
                "following":False,
                "input": "",
                "tags": []
            }
    res = [x for x in res.values()]
    res = {
        "success":True,
        "data":{"userList":res}
    }
    return HttpResponse(json.dumps(res))

def search_friends(request):
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    # f_to_id = request.GET.get('f_to')
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
        # f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_from id in db")
        return HttpResponse('not OK, no user')
    search = request.GET.get('search')
    f = Profile.objects.filter(name__contains=search).values("user__id")
    seen = [int(x['user__id']) for x in f]
    try:
        f = Friend.objects.filter(friend_from = f_from).values("friend_from", "friend_to", "tag__tag_info", "tag__id")
    except Friend.DoesNotExist:
        pass
    res = {}
    for fields in f:
        t = int(fields['friend_to'])
        if t not in seen:
            continue
        f_to = AuthUser.objects.get(id=t)
        friend = Profile.objects.filter(user=f_to).values("name", "email", "avatar")[0]
        if t not in res.keys():
            res[t] = {
                "id":t,
                "name":friend["name"],
                "email":friend["email"],
                "imgUrl": friend["avatar"],
                "following":True,
                "input": "",
                "tags": [
                    {"content":fields['tag__tag_info'], "id":fields['tag__id']}
                ]
            }
        else:
            res[t]["tags"].append({"content":fields['tag__tag_info'], "id":fields['tag__id']})
    all_user = Profile.objects.all().values("user__id", "name", "email", "avatar")
    for u in all_user:
        uid = int(u["user__id"])
        if uid not in seen:
            continue
        if uid not in res.keys():
            res[uid] = {
                "id":uid,
                "name":u["name"],
                "email":u["email"],
                "imgUrl": u["avatar"],
                "following":False,
                "input": "",
                "tags": []
            }
    res = [x for x in res.values()]
    res = {
        "success":True,
        "data":{"userList":res}
    }
    return HttpResponse(json.dumps(res))

#suoyou guanzhu wode 
def get_followers(request):
    # f_from = request.user
    f_from_id = int(request.GET.get('f_from'))
    try:
        f_from = AuthUser.objects.get(id=f_from_id)
    except AuthUser.DoesNotExist:
        print("no such f_from id in db")
        return HttpResponse('not OK')
    try:
        f = Friend.objects.filter(friend_to= f_from).values("friend_from", "friend_to", "tag__tag_info", "tag__id")
    except Friend.DoesNotExist:
        print("no such f_from id in db")
        pass
    res = {}
    for fields in f:
        t = int(fields['friend_from'])
        f_to = AuthUser.objects.get(id=t)
        friend = Profile.objects.filter(user=f_to).values("name", "email", "avatar")[0]
        if t not in res.keys():
            res[t] = {
                "id":t,
                "name":friend["name"],
                "email":friend["email"],
                "imgUrl": friend["avatar"],
                "input": "",
                "tags": [
                    # {"content":fields['tag__tag_info'], "id":fields['tag__id']}
                ]
            }
        # else:
        #     res[t]["tags"].append({"content":fields['tag__tag_info'], "id":fields['tag__id']})
    res = [x for x in res.values()]
    res = {
        "success":True,
        "data":{"userList":res}
    }
    return HttpResponse(json.dumps(res))

# get all posts that you are allowed to see
def get_visible_posts(request):
    user_id = int(request.GET.get('user'))
    try:
        user= AuthUser.objects.get(id=user_id)
    except AuthUser.DoesNotExist:
        print("no such user id in db")
        return HttpResponse('not OK')
    # who I follow
    i_follow = Friend.objects.filter(friend_from=user).values('friend_to__id')
    i_follow_ids = [int(x['friend_to__id']) for x in i_follow]
    print("follow_ids:", i_follow_ids)
    # get all tags
    tags = Friend.objects.filter(friend_to=user, friend_from__id__in=i_follow_ids).select_related('tag')
    for tag in tags:
        print(tag.tag.id, tag.tag.tag_info)
    # get all posts
    res = None
    for t in tags:
        if res == None:
            p = PostTag.objects.filter(tag=t.tag).select_related("post")
            res = [int(x["post__id"]) for x in p.values("post__id")] 
        else:
            p = PostTag.objects.filter(tag=t.tag).select_related("post")
            res += [int(x["post__id"]) for x in p.values("post__id")]
    if res == None:
        print("no tag")
        return HttpResponse(json.dumps([]))
    # ids = [int(x["post__id"]) for x in res.values("post__id")]
    ids = res
    print(ids)
    p = Post.objects.filter(author=user)
    for x in p:
        if int(x.id) not in ids:
            ids.append(int(x.id))
    q = Post.objects.filter(id__in=ids).order_by("-create_time")
    res = [PostSerializer(x).data for x in q]
    # print(res)
    for x in res:
        author = x['author']
        p = Profile.objects.get(user__id=int(author))
        x['imgUrl'] = p.avatar
        x['name'] = p.name
        for c in x['comments']:
            author = int(c['author'])
            p = Profile.objects.get(user__id=int(author))
            c['imgUrl'] = p.avatar
            c['name'] = p.name
    # json = JSONRenderer().render(res.data)
    js = json.dumps(res)
    # js = 0
    return HttpResponse(js)

# get all posts for a certain user that you can see
def get_visible_posts_of_one(request):
    user_id = int(request.GET.get('user'))
    f_to_id = int(request.GET.get('f_to'))
    try:
        user= AuthUser.objects.get(id=user_id)
    except AuthUser.DoesNotExist:
        print("no such user id in db")
        return HttpResponse('not OK')
    try:
        f_to = AuthUser.objects.get(id=f_to_id)
    except AuthUser.DoesNotExist:
        print("no such f_to id in db")
        return HttpResponse('not OK')
    # get all tags
    tags = []
    if user_id != f_to_id:
        tags = Friend.objects.filter(friend_to=user, friend_from=f_to).select_related('tag')
        # print(tags)
        # get all posts
        res = None
        for t in tags:
            if res == None:
                p = PostTag.objects.filter(tag=t.tag).select_related("post")
                res = [int(x["post__id"]) for x in p.values("post__id")]
            else:
                p = PostTag.objects.filter(tag=t.tag).select_related("post")
                res += [int(x["post__id"]) for x in p.values("post__id")]
        if res == None:
            print("no tag")
            return HttpResponse(json.dumps([]))
        # ids = [int(x["post__id"]) for x in res.values("post__id")]
        ids = res
        # p = Post.objects.filter(author=user)
        # for x in p:
        #     if int(x.id) not in ids:
        #         ids.append(int(x.id))
        q = Post.objects.filter(id__in=ids).order_by("-create_time")
    else:
        q = Post.objects.filter(author=user).order_by("-create_time")
    res = [PostSerializer(x).data for x in q]
    # print(res)
    for x in res:
        author = x['author']
        p = Profile.objects.get(user__id=int(author))
        x['imgUrl'] = p.avatar
        x['name'] = p.name
        for c in x['comments']:
            author = int(c['author'])
            p = Profile.objects.get(user__id=int(author))
            c['imgUrl'] = p.avatar
            c['name'] = p.name
    js = json.dumps(res)
    # js = 0
    return HttpResponse(js)

# make comments
def make_comment(request):
    user_id = int(request.GET.get('user'))
    try:
        user= AuthUser.objects.get(id=user_id)
    except AuthUser.DoesNotExist:
        print("no such user id in db")
        return HttpResponse('not OK')
    post_id = int(request.GET.get('post_id'))
    content = int(request.GET.get('content'))
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("no such post id in db")
        return HttpResponse('not OK')
    PostComment.objects.update_or_create(author = user, post = post, content = content)

# new post
def new_post(request):
    author_id = int(request.GET.get('author'))
    content = request.GET.get('content')
    tags = request.GET.getlist('tags')
    print(tags)
    try:
        author = AuthUser.objects.get(id=author_id)
    except AuthUser.DoesNotExist:
        print("no such f_from or f_to id in db")
        return HttpResponse('not OK')
    p, _ = Post.objects.update_or_create(author=author, content=content)
    for tag_id in tags:
        try:
            tag = Tag.objects.get(id=int(tag_id), user = author)
        except Tag.DoesNotExist:
            continue
        PostTag.objects.update_or_create(post=p, tag=tag) 
    return HttpResponse('OK')

# delete_post
def delete_post(request):
    post_id = int(request.GET.get("post"))
    try:
        p = Post.objects.get(id=int(post_id))
        p.delete()
    except Post.DoesNotExist:
        pass
    return HttpResponse('OK')

def delete_comment(request):
    comment_id = int(request.GET.get("post"))
    try:
        comment = PostComment.objects.get(id=int(comment_id))
        comment.delete()
    except PostComment.DoesNotExist:
        pass
    return HttpResponse('OK')

def get_all_tags_of_one_user(request):
    user_id = int(request.GET.get("user_id"))
    try:
        user = AuthUser.objects.get(id=user_id)
    except:
        print("no such user id in db")
        return HttpResponse('not OK')
    tags = Tag.objects.filter(user=user)
    res = [TagSerializer(x).data for x in tags]
    return HttpResponse(json.dumps(res))
    
# TSH end
# ZJN

# ZJN end