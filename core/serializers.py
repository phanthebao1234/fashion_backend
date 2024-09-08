from rest_framework import serializers
from .models import Category, Brand, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'imageUrl')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title', 'imageUrl')
        
from .models import Brand, Category, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # Use the imported Product model
        fields = '__all__'