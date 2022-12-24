from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        read_only_fields = ('author',)
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        read_only_fields = ('author', "post")
        model = Comment
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.username


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Follow
