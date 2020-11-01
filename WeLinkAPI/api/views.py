from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
)
from .util import login
from .models import Post

from django.http import HttpResponse, HttpResponseRedirect
from .util import login

def index(request):
    return HttpResponse("Hello, world! You can post your life here!<br>"+request.session['oauth_struct'])

def callback(request):
    return login.redirect_back(request)

def login_test(request):
    # del request.session['oauth_struct']
    res = login.request_auth(request)
    return HttpResponseRedirect(str(res))

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'api/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'api/home.html'
    context_object_name = 'posts'
    ordering = ['-post_date']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    # set default post author as the logged user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    # Check if is logged
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
