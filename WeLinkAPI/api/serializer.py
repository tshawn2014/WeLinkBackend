from django.urls import path, include
from .models import Profile, Post, PostComment, PostLike, Friend, Tag, PostTag
from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers

# Serializers define the API representation.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class PostCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostComment
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    comments = PostCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"



class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class FriendSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    class Meta:
        model = Friend
        fields = "__all__"


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = "__all__"


