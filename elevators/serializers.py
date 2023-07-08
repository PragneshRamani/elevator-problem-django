from rest_framework import serializers
from .models import Elevator, Floor, Request

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = ['id', 'is_operational', 'is_maintenance', 'current_floor', 'direction']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'floor_number']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'