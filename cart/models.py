from django.db import models
from django.contrib.auth.models import User
from core.models import Product
from django.utils import timezone

class Cart(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=100, blank=False)
    color = models.CharField(max_length=100, blank=False) 
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:  # sourcery skip: use-fstring-for-formatting
        return '{}/{}'.format(self.userId.username, self.product.title)