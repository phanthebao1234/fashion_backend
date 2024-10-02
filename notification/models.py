from django.contrib.auth.models import User
from order.models import Order

from django.db import models

class Notification(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=255)
    isRead = models.BooleanField(default=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f'{self.userId.username} | {self.userId.id}'