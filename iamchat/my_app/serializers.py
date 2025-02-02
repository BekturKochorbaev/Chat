from rest_framework import serializers
from .models import BotResponse


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4096)


class BotResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField('%d-%m-%Y, %H:%M')

    class Meta:
        model = BotResponse
        fields = ['response', 'created_at']