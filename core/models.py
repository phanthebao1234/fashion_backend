from django.db import models
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    imageUrl = models.ImageField(blank=False)
    
    def __str__(self) -> str:
        return self.title
    
class Brand(models.Model):
    title = models.CharField(max_length=200, unique=True)
    imageUrl = models.ImageField(blank=False)
    
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=255,)
    description = models.TextField(max_length=555)
    price = models.FloatField(default=0, blank=False)
    is_featured = models.BooleanField(default=False)
    clothesType = models.TextField(max_length=255, default='unisex')
    ratting = models.FloatField(blank=False, default=1.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    colors = models.JSONField(blank=True)
    sizes = models.JSONField(blank=True)
    imageUrl = models.JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    
    def __str__(self) -> str:
        return self.title
    
        