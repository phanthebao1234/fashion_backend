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
    """Định nghĩa 1 APIVIEW để tạo 1 đơn hàng và yêu cầu người dùng xác thực để truy cập endpoint này.

    Returns:
        id: order id
    """
    # đảm bảo rằng chỉ những người dùng đã xác thực mới có thể truy cập view này.
    permission_classes = [IsAuthenticated]
    
    # Phương thức này xử lý các yêu cầu POST để tạo một đơn hàng mới.
    def post(self, request):
        
        # Dữ liệu từ yêu cầu được trích xuất và lưu trữ trong biến data.
        data = request.data
        
        try:
            # Điều này đảm bảo rằng tất cả các thao tác cơ sở dữ liệu trong khối này là nguyên tử, 
            # nghĩa là chúng hoặc tất cả thành công hoặc tất cả thất bại.
            with transaction.atomic():
                # Mỗi sản phẩm trong đơn hàng được xác thực bằng cách kiểm tra xem nó có tồn tại trong cơ sở dữ liệu hay không. 
                # Nếu không tìm thấy sản phẩm, một lỗi 404 sẽ được trả về.
                validated_products = []
                
                for product_data in data['order_products']:
                    product = get_object_or_404(Product, id=product_data['product'])
                
                # Chi tiết sản phẩm đã xác thực được thêm vào danh sách validated_products.
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
                
                # Địa chỉ được xác thực bằng cách kiểm tra xem nó có tồn tại trong cơ sở dữ liệu hay không.
                address = get_object_or_404(Address, id = int(data['address']))
                
                # Một đơn hàng mới được tạo với dữ liệu đã xác thực.
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
                
                # create notification 
                # Một thông báo được tạo để thông báo cho người dùng rằng đơn hàng của họ đã được đặt thành công.
                title = "Order Successfully Placed"
                message = "Your payment has been successfully and your order has been successfully placed"
                Notification.objects.create(orderId=order , title=title, message=message, userId = request.user)
                
                # Lưu đơn hàng và csdl
                order.save()
                
                # Một phản hồi được trả về với ID của đơn hàng và trạng thái 201 (Đã tạo).
                return Response({"id": order.id}, status = status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            # Nếu không tìm thấy bất kỳ sản phẩm nào, một phản hồi 404 sẽ được trả về.
            return Response({"message": "one or more product not found"}, status = status.HTTP_404_NOT_FOUND)
        
        except Address.DoesNotExist:
            # Nếu không tìm thấy địa chỉ, một phản hồi 404 sẽ được trả về.
            return Response({"message": "user address does not exist"}, status = status.HTTP_404_NOT_FOUND)
        
        except KeyError as e:
            # Nếu thiếu bất kỳ khóa nào cần thiết từ dữ liệu yêu cầu, 
            # một phản hồi 400 sẽ được trả về với thông tin về khóa bị thiếu.
            return Response({"message": f"Missing key: {str(e)}"}, status = status.HTTP_400_BAD_REQUEST) 
        
class UserOrdersByStatus(APIView):
    """ Định nghĩa một API view trong Django để lấy danh sách order theo trạng thái.

    Args:
        APIView (none): none

    Returns:
        order: list order
    """
    
    # Điều này đảm bảo rằng chỉ những người dùng đã xác thực mới có thể truy cập view này.
    permission_classes = [IsAuthenticated]
    
    # Phương thức này xử lý các yêu cầu GET để lấy danh sách các đơn hàng của người dùng theo trạng thái.
    def get(self, request):
        # Trạng thái đơn hàng được lấy từ các tham số truy vấn của yêu cầu và lưu trữ trong biến order_status.
        order_status = request.query_params.get['status']
        
        # lấy thông tin người dùng
        user =request.user
        
        # truy vấn models Order lọc ra đối order có delivery_status = order_status và sắp xếp ngày tạo theo thự tự giảm dần
        orders = models.Order.objects.filter(user=user, delivery_status=order_status).order_by("-created_at")
        
        # tuần tự hóa dữ liệu
        # Đoạn này khởi tạo OrderSerializer với các đơn hàng đã được lọc. 
        # Tham số many=True cho biết rằng có nhiều đối tượng đơn hàng đang được tuần tự hóa.
        serializer = serializers.OrderSerializer(orders, many = True)
        
        # Cuối cùng, đoạn này trả về dữ liệu đã được tuần tự hóa dưới dạng phản hồi JSON với mã trạng thái HTTP 200 (OK).
        return Response(serializer.data, status=status.HTTP_200_OK)

        