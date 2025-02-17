from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4096)


class BotResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField('%d-%m-%Y, %H:%M')

    class Meta:
        model = BotResponse
        fields = ['response', 'created_at']


class GenerateSlideInputSerializer(serializers.Serializer):
    keyword = serializers.CharField(help_text="Ключевое слово для генерации слайдов")
    count = serializers.IntegerField(
        help_text="Количество слайдов (1 или 2)",
        min_value=1,
        max_value=2,
        default=1
    )


class SlideFirstSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideFirst
        fields = '__all__'


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'