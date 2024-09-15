from . import views
from django.urls import path

urlpatterns = [
    path('me/', views.GetUserCart.as_view(), name='get-user-cart'),
    path('add/', views.AddItemToCart.as_view(), name='add-item-to-cart'),
    path('count/', views.CartCount.as_view(), name='count'),
    path('delete/', views.RemoveItemFormCart.as_view(), name='delete'),
    path('update/', views.UpdateCartItemQuantity.as_view(), name='update-count'),
]
