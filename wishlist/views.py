from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import serializers, models

class GetWishList(generics.ListAPIView):
    serializer_class = serializers.WishListSerializer
    permission_classes = [IsAuthenticated,]
    queryset = models.WishList.objects.all()
    
    def get_queryset(self):
        return models.WishList.objects.filter(userId = self.request.user)
    
class ToggleWishList(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        user_id = request.user.id
        product_id = request.query_params.get('id')

        if not user_id or not product_id:
            return Response({'message': 'Invalid Request a user id and product id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST) 

        wishlist_item, created = models.WishList.objects.get_or_create(userId = request.user, product = product)

        if created:
            return Response({'message': 'Product added to wish list'}, status=status.HTTP_201_CREATED)
        wishlist_item.delete()
        return Response({'message': 'Product remove from wish list'}, status=status.HTTP_204_NO_CONTENT)
        