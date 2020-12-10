from django.contrib import admin

# Register your models here.
from .models import Profile, Post, PostComment, PostLike, PostTag, Tag, Friend

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(PostTag)
admin.site.register(Tag)
admin.site.register(Friend)