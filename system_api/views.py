from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response


from . import serializers
from production import models

# Create your views here.
class ListCreateOrder(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

class RetrieveUpdateDestroyOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

class ListCreatePiece(generics.ListCreateAPIView):
    queryset = models.Piece.objects.all()
    serializer_class = serializers.PieceSerializer

    def get_queryset(self):
        return self.queryset.filter(order_slug=self.kwargs.get('order_pk'))

class RetrieveUpdateDestroyPiece(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Piece.objects.all()
    serializer_class = serializers.PieceSerializer