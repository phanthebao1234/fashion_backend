from rest_framework import serializers
from . import models
from core.serializers import ProductSerializer

class CartSerializer(serializers.Serializer):
    product = ProductSerializer
    
    class Meta:
        models = models.Cart
        exclude = ['userId', 'created_at', 'updated_at']