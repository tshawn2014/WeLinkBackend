from django.urls import path, include
from .models import Profile, Post, PostComment, PostLike
from rest_framework import serializers

# Serializers define the API representation.
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"

class PostLikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

