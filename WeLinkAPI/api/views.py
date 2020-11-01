from django.shortcuts import render
from .util import login

from django.http import HttpResponse, HttpResponseRedirect
from .util import login

def index(request):
    return HttpResponse("Hello, world! You can post your life here!<br>"+request.session['oauth_struct'])

def callback(request):
    return login.redirect_back(request)

def login_test(request):
    # del request.session['oauth_struct']
    res = login.request_auth(request)
    return HttpResponse(str(res))

def rcmk(request):
    del request.session['oauth_struct']
    return HttpResponse('Removed')