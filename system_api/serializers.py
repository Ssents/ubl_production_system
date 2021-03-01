from rest_framework import serializers
from production import models

class OrderSerializer(serializers.ModelSerializer):
    class Meta:

        read_only_fields = ('order_slug',)

        fields = (
            "id",
            "order_slug",
            "production_type",
            "production_bond",
            "profile",
            "order_number",
            "order_colour",
            "order_colour",
            "order_finish",
            "order_gauge",
            "order_width",
            "date_received"

        )
        model = models.Order

class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "order_slug",
            "prime_pieces",
            "reject_pieces"

        )
        model = models.Piece
