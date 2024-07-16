from rest_framework import serializers
from .models import Delivery

class  DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['order_id', 'delivery_provider','current_location','delivery_method','status']
        read_only_fields = ['id','created_at', 'updated_at']
