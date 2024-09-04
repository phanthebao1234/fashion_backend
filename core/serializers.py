from rest_framework import serializers
from . import models

class CaterogySerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Category
        fields = ('id', 'title', 'imageUrl')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Category
        fields = ('id', 'title', 'imageUrl')
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Product
        fields = (
            'id', 
            'title', 
            'description', 
            'price', 
            'is_featured',  
            'clothesType',
            'ratting',
            'caterogy',
            'brand',
            'colors',
            'sizes',
            'imageUrl', 
            'created_at',
            )
        