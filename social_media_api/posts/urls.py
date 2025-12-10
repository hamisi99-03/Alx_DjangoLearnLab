from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Explicit feed path
    path('feed/', PostViewSet.as_view({'get': 'feed'}), name='feed'),

    # Router endpoints (posts/, comments/, etc.)
    path('', include(router.urls)),
]