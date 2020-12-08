from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .util import login
from .models import Post, Profile, PostComment, PostLike

from django.http import HttpResponse, HttpResponseRedirect
from .util import login
from rest_framework import viewsets, generics, filters
from .serializer import ProfileSerializer, PostSerializer, PostLikeSerializer, PostCommentSerializer

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
    del request.session['oauth_struct']
    return HttpResponse("Removed.")

# rest_framework related
class ProfileViewSet(viewsets.ModelViewSet):
    search_fields = ['email', 'name']
    filter_backends = (filters.SearchFilter,)
    queryset = Profile.objects.all().order_by('email')
    serializer_class = ProfileSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('create_time')
    serializer_class = PostSerializer

class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer

class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
# TSH end