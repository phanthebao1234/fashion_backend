from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import models, serializers

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notifications = models.Notification.objects.filter(userId=request.user, isRead=False).order_by('-created_at')
        serializer = serializers.NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class GetDetailNotification(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        _id = request.query_params.get('id')
        notifications = models.Notification.objects.filter(userId=request.user, id=_id, isRead=False).order_by('-created_at')
        serializer = serializers.NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
class GetCountNotification(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        unread_count = models.Notification.objects.filter(userId=request.user).count()
        
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)
    
class UpdateNotification(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        if not (notification_id := request.query_params.get('id')):
            return Response({'message': 'Notification id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            notification = models.Notification.objects.get(id=notification_id)
            notification.isRead = True
            notification.save()

            return Response({'message': 'Updated notification successfully'}, status=status.HTTP_200_OK)
        except models.Notification.DoesNotExist:
            return Response({'message': 'Notification does not exist'}, status=status.HTTP_400_BAD_REQUEST)