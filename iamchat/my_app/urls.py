from django.urls import path
from .views import *

urlpatterns = [
    path('websocket-info/', WebSocketInfoView.as_view(), name='websocket-info'),
    path("answers/", GetBotResponsesAPIView.as_view(), name="get-answers"),

]