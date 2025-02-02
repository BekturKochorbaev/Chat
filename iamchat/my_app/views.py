from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BotResponse
from .serializers import BotResponseSerializer

class WebSocketInfoView(APIView):
    """
    Отображает описание WebSocket подключения
    """
    def get(self, request, *args, **kwargs):
        return Response({
            "websocket": "ws://localhost:8000/ws/chat/",  # Ваш WebSocket URL
            "description": "Use this WebSocket URL to connect to the chat."
        }, status=status.HTTP_200_OK)


class GetBotResponsesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        responses = BotResponse.objects.all()
        serializer = BotResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
