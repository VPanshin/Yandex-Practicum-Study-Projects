"""Serializers for API application."""

import base64

from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(serializers.ImageField):
    """Class to encode image file into Base64 binary data."""

    def to_internal_value(self, data):
        """Create a file from decoding image from Base64."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Serializers class for Post model to convert data in JSON format."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    image = Base64ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Serializers class for Group model to convert data in JSON format."""

    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """Serializers class for Comment model to convert data in JSON format."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post', )


class FollowSerializer(serializers.ModelSerializer):
    """Serializers class for Follow model to convert data in JSON format."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, data):
        """Check if User is trying to follow themselves."""
        if self.context['request'].user == data:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя')
        return data