from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from . import serializers
from posts.models import Group, Post, Comment, Follow

from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly]

    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class CreateRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class FollowViewSet(CreateRetrieveViewSet):
    serializer_class = serializers.FollowSerializer
    search_fields = ('following__username',)
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # if Follow.objects.filter(
        #         user=self.request.user,
        #         following=serializer.validated_data.get('following')):
        #     raise ParseError('Запись уже существует')
        #
        # if serializer.validated_data.get(
        #         'following') == self.request.user:
        #     raise ParseError('Невозможно подписаться на самого себя')
