from django.contrib import admin

# Register your models here.
from .models import User, Post, PostComment, PostLike

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostLike)