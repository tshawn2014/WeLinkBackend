from django.shortcuts import render
from .util import login

from django.http import HttpResponse, HttpResponseRedirect
from .util import login

def index(request):
    return HttpResponse("Hello, world! You can post your life here!"+request.session['oauth_struct'])

def callback(request):
    return login.redirect_back(request)

def login_test(request):
    res = login.request_auth(request)
    return HttpResponseRedirect(str(res))