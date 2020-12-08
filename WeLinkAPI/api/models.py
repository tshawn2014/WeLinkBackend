from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

class Profile(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=200)
    avatar = models.ImageField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login',
        null=True
    )
    # access_token: authorization for canvas api
    access_token = models.TextField(null=True)
    # refresh_token: if expire, use this to refresh
    refresh_token = models.TextField(null=True)
    # expires: expiration time
    expires = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def expires_within(self, delta):
        """
        Check token expiration with timezone awareness within
        the given amount of time, expressed as a timedelta.

        :param delta: The timedelta to check expiration against
        """
        if not self.expires:
            return False

        return self.expires - timezone.now() <= delta

    def __str__(self):
        return "%s" % self.user

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_time = models.TimeField(auto_now_add=True, editable=False)
    update_time = models.TimeField(auto_now_add=True, editable=False, null=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('api-home')

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_time = models.TimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.content

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.TimeField(auto_now_add=True, editable=False)

class Friend(models.Model):
    friend_from = models.ForeignKey(User, related_name='friend_from',on_delete=models.CASCADE)
    friend_to = models.ForeignKey(User, related_name='friend_to',on_delete=models.CASCADE)
    tag_info = models.CharField(max_length=20, null=True)
    create_time = models.TimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.friend_from.username) + ' tag ' + str(self.friend_to.username) + ' as ' + self.tag_info

