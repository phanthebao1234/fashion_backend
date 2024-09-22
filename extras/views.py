from . import models, serializers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

class AddAdress(APIView):
    permission_classes = [IsAuthenticated] 
    
    def post(self, request):
        data = request.data
        
        user_address = models.Address.objects.create(
            userId = request.user,
            lat = data['lat'],
            lng = data['lng'],
            isDefault = data['isDefault'],
            address = data['address'],
            phone = data['phone'],
            addressType = data['addressType'],
        )
        
        if user_address.isDefault == True:
            models.Address.objects.filter(userId = request.user).update(isDefault = False)
            
        user_address.save()
        return Response(status=status.HTTP_201_CREATED)
    
class GetUserAddress(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        addresess = models.Address.objects.filter(userId= request.user)
        serializer = serializers.AddressSerializer(addresess, many=True)
        return Response(serializer.data)
    
class GetDefaultAddress(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        addresses = models.Address.objects.filter(userId= request.user, isDefault=True)
        
        if addresses.exists():
            addresses = addresses.first()
            serializer = serializers.AddressSerializer(addresses)
            return Response(serializer.data)
        else:
            return Response({'message': 'No default address found'}) 

class DeleteAddress(APIView):
    """Xóa địa chỉ mặc định cũ và thay thế địa chỉ mặc định mới

    Returns:
        _type_: new address/status code 400
    """
    # lớp xác thực người dùng
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        # lấy id address từ param id
        address_id = request.query_params.get('id')

        # nếu không có id => No id provided
        if not address_id:
            return Response({'message': 'No id provided'})

        try:
            # lấy thông tin người dùng
            user= request.user

            # tìm địa chỉ với id và userId tương ứng
            address_item = models.Address.objects.get(id=address_id, userId=user)

            # bắt đầu giao dịch để đảm bảo tính toàn vẹn dữ liệu
            with transaction.atomic():
                # nếu địa chỉ là mặc định thì gọi phương thức _extracted_from_delete_ để xử lý
                if address_item.isDefault:
                    return self._extracted_from_delete_(user, address_id, address_item)
        # nếu không có địa chỉ => Address not foud
        except models.Address.DoesNotExist:
            return Response({'message': 'Address not found'}, status=status.HTTP_400_BAD_REQUEST) 

    #  phương thức này được gọi khi xóa địa chỉ mặc định
    def _extracted_from_delete_(self, user, address_id, address_item):
        # lấy tất cả address của user ngoại trừ địa chỉ đang xóa là address_id nhận được ở trên
        ortherAddress = models.Address.objects.filter(userId=user).exclude(id=address_id)
        
        # nếu không có địa chỉ nào khác thì => không thể xóa địa chỉ mặc định khi không có các địa chỉ khác
        if not ortherAddress.exists:
            return Response({'message': 'You can not delete a default address without any other address'})

        # lấy địa chỉ khác ở vị trí đầu tiên 
        new_default_address = ortherAddress.first()
        # để địa chỉ đó làm mặc định
        new_default_address.isDefault = True
        # lưu vào csdl địa chỉ mặc định mới
        new_default_address.save()
        # xóa địa chỉ cũ
        address_item.delete()
        
        # trả về phản hồi thành công
        return Response(status=status.HTTP_200_OK) 
    
class SetDefaultAddress(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        address_id = request.query_params.get('id')

        if not address_id:
            return Response({'message':'No id provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            return self.update_address_default(request, address_id)
        except models.User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    def update_address_default(self, request, address_id):
        user = request.user
        address = models.Address.objects.get(id=address_id)
        models.Address.objects.filter(userId=user).update(isDefault=False)
        address.isDefault = True
        address.save()
        return Response({'message':'Address updated successfully'}, status=status.HTTP_200_OK)