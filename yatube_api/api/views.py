from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.pagination import LimitOffsetPagination

from . import serializers
from posts.models import Group, Post, Comment, Follow


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

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
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))

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


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FollowSerializer
    search_fields = ('following__username',)
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if Follow.objects.filter(
                user=self.request.user,
                following=serializer.validated_data.get('following')):
            raise ParseError('Запись уже существует')

        if serializer.validated_data.get(
                'following') == self.request.user:
            raise ParseError('Невозможно подписаться на самого себя')

        serializer.save(user=self.request.user)
