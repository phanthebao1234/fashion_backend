from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.NotificationListView.as_view(), name='get-notification'),
    path('count/', views.GetCountNotification.as_view(), name='count-notification'),
    path('update/', views.UpdateNotification.as_view(), name='update-notification'),
    path('detail/', views.GetDetailNotification.as_view(), name='detail-notification')
]
