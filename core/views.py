from rest_framework import generics, status
from . import models, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
import random

class CaterogyList(generics.ListAPIView): 
    # ListAPIView: hiển thị danh sách đối tượng
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    
class HomeCaterogyList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    
    def get_queryset(self):
        # Lấy tất cả các đối tượng Category từ cơ sở dữ liệu.
       queryset = models.Category.objects.all()
       
        # Thêm một trường chú thích random_order vào mỗi đối tượng trong queryset, 
        # giá trị của trường này là số lượng id.    
       queryset = queryset.annotate(random_order=Count('id'))
       
        # Chuyển đổi queryset thành một danh sách.
       queryset = list(queryset)
       
        # Trộn ngẫu nhiên các phần tử trong danh sách queryset.
       random.shuffle(queryset)
       
        # Trả về 5 phần tử đầu tiên của danh sách queryset đã được trộn ngẫu nhiên.
       return queryset[:5]
       

class BrandList(generics.ListAPIView): 
    # ListAPIView: hiển thị danh sách đối tượng
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()
    
class ProductList(generics.ListAPIView): 
    # ListAPIView: hiển thị danh sách đối tượng
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    
    def get_queryset(self):
        # Lấy tất cả các đối tượng Product từ cơ sở dữ liệu.
       queryset = models.Product.objects.all()
       
        # Thêm một trường chú thích random_order vào mỗi đối tượng trong queryset, 
        # giá trị của trường này là số lượng id.    
       queryset = queryset.annotate(random_order=Count('id'))
       
        # Chuyển đổi queryset thành một danh sách.
       queryset = list(queryset)
       
        # Trộn ngẫu nhiên các phần tử trong danh sách queryset.
       random.shuffle(queryset)
       
        # Trả về 20 phần tử đầu tiên của danh sách queryset đã được trộn ngẫu nhiên.
       return queryset[:20]
   
class PopularProductList(generics.ListAPIView): 
    # ListAPIView: hiển thị danh sách đối tượng
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    
    def get_queryset(self):
        # Lấy tất cả các đối tượng Product từ cơ sở dữ liệu.
       queryset = models.Product.objects.filter(ratings__gte=4.0, ratings__lte=5.0)
       
        # Thêm một trường chú thích random_order vào mỗi đối tượng trong queryset, 
        # giá trị của trường này là số lượng id.    
       queryset = queryset.annotate(random_order=Count('id'))
       
        # Chuyển đổi queryset thành một danh sách.
       queryset = list(queryset)
       
        # Trộn ngẫu nhiên các phần tử trong danh sách queryset.
       random.shuffle(queryset)
       
        # Trả về 20 phần tử đầu tiên của danh sách queryset đã được trộn ngẫu nhiên.
       return queryset[:20]
   
class PopularProductListByClothesType(APIView): 
    # ListAPIView: hiển thị danh sách đối tượng
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    
    def get(self, request):
        query = request.query_params.get('clothesType', None)

        if query:
            queryset = models.Product.objects.filter(clothesType=query)
            queryset = queryset.annotate(random_order=Count('id'))
        
            product_list = list(queryset)
            random.shuffle(product_list)
            
            limited_product = product_list[:20]
            
            serializer = serializers.ProductSerializer(limited_product, many=True)
            
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)

class SimilarProduct(APIView):
    def get(self, request):
        query = request.query_params.get('category', None)
        
        if query:
            products = models.Product.objects.filter(category=query)
            product_list = list(products)
            random.shuffle(product_list)
            
            limited_product = product_list[:6]
            serializer = serializers.ProductSerializer(limited_product, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class SearchProductByTitle(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)
        
        if query:
            products = models.Product.objects.filter(title__icontains=query)
            
            serializer = serializers.ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class FilterProductByCategory(APIView):
    def get(self, request):
        query = request.query_params.get('category', None)
        
        if query:
            products = models.Product.objects.filter(category=query)
            
            serializer = serializers.ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        