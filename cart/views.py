from django.db import models
from .models import Cart, Product
from .serializers import CartSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response

class AddItemToCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        
        try:
            product = Product.objects.get(id = data['product'])
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND) 
        
        try:
            # check cart nếu trùng product id, color và size thì sẽ tăng quantity của cart 
            cart_item = Cart.objects.get(
                userId = user,
                product = product ,
                color = data['color'],
                size = data['size']
            )
            
            cart_item.quantity += data.get('quantity', 1)
            cart_item.save()
            # sau đó return về message
            return Response({'message': 'Item updated to the cart'}, status = status.HTTP_200_OK)
        
            # nếu đó là product id không có trong cart hoặc có các size và color khác với sản phẩm trùng product id thì sẽ tạo 1 cart mới
        except Cart.DoesNotExist:
            newCart = Cart.objects.create(
                userId = user,
                product = product,
                color = data['color'],
                size = data['size'],
                quantity = data.get('quantity', 1),
            )
            return Response({'message': 'Item added to the cart'}, status = status.HTTP_201_CREATED)
    
class RemoveItemFormCart(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        if cart_id := request.query_params.get('id'):
            cart_items = Cart.objects.filter(userId = user)
            
            if not cart_items.filter(id=cart_id).exists():
                return Response({'message': 'Cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            cart_items.filter(id=cart_id).delete()
            return Response({'message': 'Item removed successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Cart id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
class CartCount(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        cart_count = Cart.objects.filter(userId = user).count()
        return Response({'cart_count': cart_count}, status=status.HTTP_200_OK)
    
class UpdateCartItemQuantity(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        item_id = request.query_params.get('id')
        count = request.query_params.get('count')
        print(count)
        
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.quantity = count
        cart_item.save()
        
        return Response({'message': 'Cart Item updated successfully'}, status=status.HTTP_200_OK)
    
class GetUserCart(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(userId = user).order_by('-created_at')
        
        serializer = CartSerializer(cart_items, many = True)
        return Response(serializer.data)
        
        