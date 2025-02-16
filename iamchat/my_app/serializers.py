from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4096)


class BotResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField('%d-%m-%Y, %H:%M')

    class Meta:
        model = BotResponse
        fields = ['response', 'created_at']

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'

    def to_representation(self, instance):
        # Получаем стандартное представление объекта
        representation = super().to_representation(instance)

        # Удаляем поля с null значениями
        for key in list(representation.keys()):
            if representation[key] is None:
                del representation[key]

        return representation