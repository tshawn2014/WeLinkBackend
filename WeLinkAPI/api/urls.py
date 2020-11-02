from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDeleteView,
    rmck,
    login_test,
    callback,
    index,
)

urlpatterns = [
    path('login', login_test, name='login_test'),
    path('oauth2callback', callback, name='oauth2callback'),
    path('rmck', rmck, name='rmck'),
    path('index', index, name='index'),
    path('', PostListView.as_view(), name='api-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]