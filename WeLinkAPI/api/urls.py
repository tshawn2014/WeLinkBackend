from django.urls import path, include
from .views import (
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    rmck,
    login_test,
    callback,
    index,
)
from rest_framework import routers
from .views import PostViewSet, ProfileViewSet, PostLikeViewSet, PostCommentViewSet, AuthUserViewSet,FriendViewSet, TagViewSet, PostTagViewSet
from .util.login import request_auth
from .util.actions import (add_friends, delete_friends, 
        get_friends, add_tag, get_visible_posts, 
        remove_tag, get_visible_posts_of_one, 
        get_followers, new_post, delete_post, 
        get_all_tags_of_one_user,
        delete_comment,search_friends)

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', PostLikeViewSet)
router.register(r'comments', PostCommentViewSet)
router.register(r'users', AuthUserViewSet)
router.register(r'friends', FriendViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posttags', PostTagViewSet)

urlpatterns = [
    path('oauth_test/', login_test, name='login_test'),
    path('oauth2/', request_auth, name='oauth2'),
    path('oauth2callback', callback, name='oauth2callback'),
    path('follow', add_friends, name='follow'),
    path('followers', get_followers, name='followers'),
    path('followings', get_friends, name='followings'),
    path('unfollow', delete_friends, name='unfollow'),
    path('add_tag', add_tag, name='add_tag'),
    path('remove_tag', remove_tag, name='remove_tag'),
    path('newsfeed', get_visible_posts, name='newsfeed'),
    path('timeline', get_visible_posts_of_one, name='timeline'),
    path('new_post', new_post, name='new_post'),
    path('search_friends', search_friends, name='search_friends'),
    path('delete_post', delete_post, name='delete_post'),
    path('delete_comment', delete_comment, name='delete_comment'),
    path('all_tags', get_all_tags_of_one_user, name='all_tags'),
    path('rmck', rmck, name='rmck'),
    path('index', index, name='index'),
    # path('', PostListView.as_view(), name='api-home'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', include(router.urls)),
]