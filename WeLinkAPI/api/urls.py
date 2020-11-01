from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('login', views.login_test, name='login_test'),
    path('oauth2callback', views.callback, name='oauth2callback'),
    path('index', views.index, name='index'),
    path('', PostListView.as_view(), name='api-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]