from rest_framework import serializers
from . import models

class WishListSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='product.title')
    id = serializers.ReadOnlyField(source='product.id')
    description = serializers.ReadOnlyField(source='product.description')
    price = serializers.ReadOnlyField(source='product.price')
    is_featured = serializers.ReadOnlyField(source='product.is_featured')
    clothesType = serializers.ReadOnlyField(source='product.clothesType')
    ratings = serializers.ReadOnlyField(source='product.ratings')
    category = serializers.ReadOnlyField(source='product.category.id')
    brand = serializers.ReadOnlyField(source='product.brand.id')
    colors = serializers.ReadOnlyField(source='product.colors')
    sizes = serializers.ReadOnlyField(source='product.sizes')
    imageUrls = serializers.ReadOnlyField(source='product.imageUrls')
    created_at = serializers.ReadOnlyField(source='product.created_at')
    
    class Meta:
        model = models.WishList
        fields = ['id','title','description','price','is_featured','clothesType', 'ratings','category', 'brand', 'colors', 'sizes', 'imageUrls', 'created_at']  