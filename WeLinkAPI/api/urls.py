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
from .views import PostViewSet, ProfileViewSet, PostLikeViewSet, PostCommentViewSet
from .util.login import request_auth
from .util.actions import add_friends

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', PostLikeViewSet)
router.register(r'comments', PostCommentViewSet)

urlpatterns = [
    path('oauth_test/', login_test, name='login_test'),
    path('oauth2/', request_auth, name='oauth2'),
    path('oauth2callback', callback, name='oauth2callback'),
    path('add_friends', add_friends, name='add_friends'),
    path('rmck', rmck, name='rmck'),
    path('index', index, name='index'),
    path('', PostListView.as_view(), name='api-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', include(router.urls)),
]