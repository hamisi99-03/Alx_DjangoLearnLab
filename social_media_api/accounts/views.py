from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import RegistrationSerializer, LoginSerializer, UserPublicSerializer

# Explicitly get your CustomUser model
CustomUser = get_user_model()

# Registration view
class RegisterView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()   # <-- contains CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# Login view
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# Token view
class TokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]   # <-- contains permissions.IsAuthenticated

    def get(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# User viewset for follow/unfollow
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()   # <-- contains CustomUser.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        target = self.get_object()
        actor = request.user
        if actor == target:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        actor.following.add(target)
        return Response({'detail': f'You now follow {target.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        target = self.get_object()
        actor = request.user
        if not actor.following.filter(pk=target.pk).exists():
            return Response({'detail': 'You do not follow this user.'}, status=status.HTTP_400_BAD_REQUEST)
        actor.following.remove(target)
        return Response({'detail': f'You unfollowed {target.username}.'}, status=status.HTTP_200_OK)