from django.contrib.auth import get_user_model
from rest_framework import generics, status ,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import RegistrationSerializer, LoginSerializer, UserPublicSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

#login view
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class TokenView(APIView):

    def get(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
#follow unfollow viewset
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]

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

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        target = self.get_object()
        followers = target.followers.all()
        serializer = UserPublicSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        target = self.get_object()
        following = target.following.all()
        serializer = UserPublicSerializer(following, many=True)
        return Response(serializer.data)
