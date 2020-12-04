# TSH - head
from ..models import Post, User, PostComment, PostLike
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import generics
from ..serializer import UserSerializer, PostSerializer
# TSH end - head
# ZJN - head

# ZJN end - head

# TSH
class PostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Post.objects.filter(purchaser=user)
# TSH end
# ZJN

# ZJN end