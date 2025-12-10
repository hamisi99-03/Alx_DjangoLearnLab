# notifications/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        unread = self.request.query_params.get('unread')
        if unread == 'true':
            qs = qs.filter(unread=True)
        return qs

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        if notification.recipient != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        notification.unread = False
        notification.save(update_fields=['unread'])
        return Response({'detail': 'Marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return Response({'detail': 'All marked as read'}, status=status.HTTP_200_OK)