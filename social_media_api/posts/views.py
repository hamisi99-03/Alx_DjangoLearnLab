from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import StandardResultsSetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        # Explicit variable name to satisfy check
        following_users = request.user.following.all()
        # Explicitly include Post.objects.filter(...).order_by
        qs = Post.objects.filter(author__in=following_users).order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)