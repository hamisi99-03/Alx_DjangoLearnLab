
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment,Like

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author', queryset=User.objects.all(), write_only=True, required=False
    )
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author', queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_id', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
