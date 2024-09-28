from rest_framework import serializers
from . import models

class NotificationSerializer(serializers.Serializer):
    model = models.Notification
    fields = '__all__'
    