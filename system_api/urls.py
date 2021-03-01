from django.urls import path, include
from . import views

urlpatterns = [
    path('orders', views.ListCreateOrder.as_view(), name='orders_list'),
    path('orders/<int:pk>', views.RetrieveUpdateDestroyOrder.as_view(), 
        name='order_detail'),
         
    path('<int:order_pk>/pieces/', views.ListCreatePiece.as_view(), 
        name ='pieces_list'),
    path('<int:order_pk>/pieces/<int:pk>', 
        views.RetrieveUpdateDestroyPiece.as_view(), 
        name ='pieces_detail'),
]