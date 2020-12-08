from django.urls import path, include
from .models import Profile, Post, PostComment, PostLike
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

