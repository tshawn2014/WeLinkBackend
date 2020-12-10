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
from .util.actions import add_friends, delete_friends, get_friends, add_tag, get_visible_posts, remove_tag

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
    path('followers', get_friends, name='followers'),
    path('unfollow', delete_friends, name='unfollow'),
    path('add_tag', add_tag, name='add_tag'),
    path('remove_tag', remove_tag, name='remove_tag'),
    path('newsfeed', get_visible_posts, name='newsfeed'),
    path('rmck', rmck, name='rmck'),
    path('index', index, name='index'),
    # path('', PostListView.as_view(), name='api-home'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', include(router.urls)),
]