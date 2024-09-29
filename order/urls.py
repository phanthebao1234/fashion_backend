from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddOrder.as_view(), name='add-order'),
    path('me/', views.UserOrdersByStatus.as_view(), name='user-order-by-status'),
    path('single/', views.OrderDetail.as_view(), name='order-detail'),
]
