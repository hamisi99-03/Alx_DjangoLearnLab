from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, LoginView, TokenView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Auth endpoints
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenView.as_view(), name='token'),

    # Follow management explicit paths
    path('follow/<int:user_id>/', UserViewSet.as_view({'post': 'follow'}), name='follow'),
    path('unfollow/<int:user_id>/', UserViewSet.as_view({'post': 'unfollow'}), name='unfollow'),

    # Router endpoints (users/, users/{id}/ etc.)
    path('', include(router.urls)),
]