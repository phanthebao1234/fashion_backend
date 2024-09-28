from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from . import models, serializers

from core.models import Product
from extras.models import Address
from notification.models import Notification

from django.db import transaction

class AddOrder(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        
        try:
            with transaction.atomic():
                validated_products = []
                
                for product_data in data['order_products']:
                    product = get_object_or_404(Product, id=product_data['product'])
                    
                validated_products.append(
                    {
                        "product_id": product.id,
                        "imageUrl": product.imageUrl[0],
                        "title": product.title,
                        "pirce": product.pirce,
                        "quantity": product_data["quantity"],
                        "size": product_data["size"],
                        "color": product_data["color"]
                    }
                )
                
                address = get_object_or_404(Address, id = int(data['address']))
                order = models.Order.objects.create(
                    user = request.user,
                    customer_id = data['customer_id'],
                    address = address,
                    order_product = validated_products,
                    rated = [0],
                    total_quantity = data['total_quantity'],
                    subtotal = data['subtotal'],
                    total = data['total'],
                    delivery_status = data['delivery_status'],
                    payment_status = data['payment_status'],
                )
        except: