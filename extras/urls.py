from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.GetUserAddress.as_view(), name='address-list'),
    path('add/', views.AddAdress.as_view(), name='address-add'),
    path('me/', views.GetDefaultAddress.as_view(), name='address-default'),
    path('delete/', views.DeleteAddress.as_view(), name='address-delete'),
    path('default/', views.SetDefaultAddress().as_view(), name='address-set-default'),
    
]
