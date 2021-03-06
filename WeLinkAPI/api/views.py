from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .util import login
from .models import Post, Profile, PostComment, PostLike, Friend, Tag, PostTag

from django.http import HttpResponse, HttpResponseRedirect
from .util import login
from rest_framework import viewsets, generics, filters
from .serializer import ProfileSerializer, PostSerializer, PostLikeSerializer, PostCommentSerializer, AuthUserSerializer, FriendSerializer, PostTagSerializer, TagSerializer
from django.contrib.auth import logout
from django.contrib.auth.models import User as AuthUser


def index(request):
    return HttpResponse("Hello, world! You can post your life here!<br>")

def callback(request):
    return login.redirect_back(request)

def login_test(request):
    # del request.session['oauth_struct']
    res = login.request_auth(request)
    return HttpResponseRedirect(res.content)

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'api/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'api/home.html'
    context_object_name = 'posts'
    ordering = ['-create_time']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    # set default post author as the logged user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    # set default post author as the logged user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Check if is logged
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    # Check if is logged
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# TSH start
def rmck(request):
    # del request.session['oauth_struct']
    logout(request)
    return HttpResponse("Removed.")

# rest_framework related
class ProfileViewSet(viewsets.ModelViewSet):
    search_fields = ['email', 'name']
    filter_backends = (filters.SearchFilter,)
    queryset = Profile.objects.all().order_by('email')
    serializer_class = ProfileSerializer
    def get_queryset(self):
        queryset = Profile.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=int(user_id))
        return queryset

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-create_time')
    serializer_class = PostSerializer

class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer

class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

class PostTagViewSet(viewsets.ModelViewSet):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
# TSH end