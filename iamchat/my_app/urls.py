from django.urls import path
from .views import *

urlpatterns = [
    path('websocket-info/', WebSocketInfoView.as_view(), name='websocket-info'),
    path("answers/", GetBotResponsesAPIView.as_view(), name="get-answers"),
    path('generate_slide/', generate_slide, name='generate_slide'),
    path('slide_answers/', get_answers, name='slide_answers'),

]