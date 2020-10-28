from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_test, name='login_test'),
    path('oauth2callback', views.callback, name='oauth2callback'),
    path('index', views.index, name='index'),
]