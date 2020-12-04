from django.contrib import admin

# Register your models here.
from .models import Profile, Post, PostComment, PostLike

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostLike)