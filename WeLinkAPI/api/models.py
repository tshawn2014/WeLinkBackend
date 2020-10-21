from django.db import models

class User(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=200)
    avatar = models.ImageField()

class Tag(models.Model):
    tag_creating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=20)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    post_date = models.DateField(auto_now_add=True, editable=False)
    post_time = models.TimeField(auto_now_add=True, editable=False)

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    comment_date = models.DateField(auto_now_add=True, editable=False)
    comment_time = models.TimeField(auto_now_add=True, editable=False)

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_date = models.DateField(auto_now_add=True, editable=False)
    like_time = models.TimeField(auto_now_add=True, editable=False)

# class FriendRelation(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE)
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
