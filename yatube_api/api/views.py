from django.shortcuts import get_object_or_404
from posts.models import Group, Post, Comment, Follow
from rest_framework import filters
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import LimitOffsetPagination

from . import serializers
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]

    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента невозможно')
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента невозможно')
        super().perform_destroy(serializer)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]

    def get_queryset(self):
        query_set = Comment.objects.filter(
            post=self.kwargs.get('post_id'))
        return query_set

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента невозможно')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента невозможно')
        super().perform_destroy(instance)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FollowSerializer
    search_fields = ('following__username',)
    filter_backends = (filters.SearchFilter,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.instance.author == self.request.user:
            raise ValidationError(
                'Подписаться на самого себя невозможно'
            )
        serializer.save(user=self.request.user)
