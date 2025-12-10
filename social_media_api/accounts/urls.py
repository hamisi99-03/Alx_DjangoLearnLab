from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, TokenView, UserViewSet

routers = DefaultRouter()
routers.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', TokenView.as_view(), name='profile'),
    path('',include(routers.urls)),  # Include the UserViewSet routes
]