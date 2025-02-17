from rest_framework.views import APIView
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SlideFirstSerializer, SlideSerializer
import requests
from .models import *


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


API_AI = "https://7030-217-29-24-178.ngrok-free.app/v1/chat/completions"
PEXELS_API_KEY = "8BgJ7ceLcIpWfBHk76gykWAN7Q1yQe7htIjcVpUP0wNmdXad3pi0ehai"

def generate_first_slide(keyword):
    # Запрос к API AI для генерации заголовка и текста
    ai_payload = {
        "model": "models/Qwen/Qwen2.5-3B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Always respond in the following format:\n\nTitle: <title>\nBrief Description: <description>"},
            {"role": "user", "content": f"Generate a short title and a brief description about {keyword}."}
        ],
        "max_tokens": 2048,
        "stream": False
    }

    ai_response = requests.post(API_AI, json=ai_payload)
    if ai_response.status_code != 200:
        return None

    ai_output = ai_response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    # Очищаем текст от лишних меток
    if "Title:" in ai_output and "Brief Description:" in ai_output:
        title = ai_output.split("Title:")[1].split("Brief Description:")[0].strip()
        description = ai_output.split("Brief Description:")[1].strip()
    else:
        # Если формат не соответствует, используем значения по умолчанию
        title = f"Тема: {keyword}"
        description = ai_output

    # Убираем лишние символы (например, звездочки) из заголовка и описания
    title = title.replace("**", "").strip()
    description = description.replace("**", "").strip()

    # Запрос к Pexels API для поиска изображения (первое изображение, page=1)
    pexels_response = requests.get(
        f'https://api.pexels.com/v1/search?query={keyword}&per_page=1&page=1',
        headers={'Authorization': PEXELS_API_KEY}
    )
    if pexels_response.status_code != 200:
        return None

    pexels_data = pexels_response.json()
    if not pexels_data.get('photos'):
        return None

    image_url = pexels_data['photos'][0]['src']['large']

    return {
        "keyword": keyword,
        "title": title,
        "description": description,
        "image_url": image_url
    }


def generate_second_slide(keyword):
    # Запрос к API AI для генерации заголовка, подзаголовков и описаний
    ai_payload = {
        "model": "models/Qwen/Qwen2.5-3B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Always respond in the following format:\n\nTitle: <title>\nSubtitle 1: <subtitle 1>\nDescription 1: <description 1>\nSubtitle 2: <subtitle 2>\nDescription 2: <description 2>\nSubtitle 3: <subtitle 3>\nDescription 3: <description 3>\nSubtitle 4: <subtitle 4>\nDescription 4: <description 4>"},
            {"role": "user", "content": f"Generate a title, four subtitles, and descriptions for each subtitle about {keyword}."}
        ],
        "max_tokens": 2048,
        "stream": False
    }

    ai_response = requests.post(API_AI, json=ai_payload)
    if ai_response.status_code != 200:
        return None

    ai_output = ai_response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    # Обрабатываем вывод AI для извлечения заголовка, подзаголовков и описаний
    try:
        title = ai_output.split("Title:")[1].split("Subtitle 1:")[0].strip()
        subtitle_1 = ai_output.split("Subtitle 1:")[1].split("Description 1:")[0].strip()
        description_1 = ai_output.split("Description 1:")[1].split("Subtitle 2:")[0].strip()
        subtitle_2 = ai_output.split("Subtitle 2:")[1].split("Description 2:")[0].strip()
        description_2 = ai_output.split("Description 2:")[1].split("Subtitle 3:")[0].strip()
        subtitle_3 = ai_output.split("Subtitle 3:")[1].split("Description 3:")[0].strip()
        description_3 = ai_output.split("Description 3:")[1].split("Subtitle 4:")[0].strip()
        subtitle_4 = ai_output.split("Subtitle 4:")[1].split("Description 4:")[0].strip()
        description_4 = ai_output.split("Description 4:")[1].strip()
    except Exception as e:
        # Если формат не соответствует, используем значения по умолчанию
        title = f"Культура и традиции {keyword}"
        subtitle_1 = "Музыка"
        description_1 = "Традиционная турецкая музыка, народные танцы и современные жанры."
        subtitle_2 = "Кухня"
        description_2 = "Кебабы, мезе, пахлава и другие вкусные блюда."
        subtitle_3 = "Искусство"
        description_3 = "Керамика, ковры, каллиграфия и другие виды искусства."
        subtitle_4 = "Обычаи"
        description_4 = "Гостеприимство, уважение к старшим и семейные ценности."

    # Запрос к Pexels API для поиска уникального изображения (второе изображение, page=2)
    pexels_response = requests.get(
        f'https://api.pexels.com/v1/search?query={keyword}&per_page=1&page=2',
        headers={'Authorization': PEXELS_API_KEY}
    )
    if pexels_response.status_code != 200:
        return None

    pexels_data = pexels_response.json()
    if not pexels_data.get('photos'):
        return None

    image_url = pexels_data['photos'][0]['src']['large']

    return {
        "title": title,
        "subtitle_1": subtitle_1,
        "description_1": description_1,
        "subtitle_2": subtitle_2,
        "description_2": description_2,
        "subtitle_3": subtitle_3,
        "description_3": description_3,
        "subtitle_4": subtitle_4,
        "description_4": description_4,
        "image_url": image_url
    }


@api_view(['POST'])
def generate_slide(request):
    input_serializer = GenerateSlideInputSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    keyword = input_serializer.validated_data['keyword']
    count = input_serializer.validated_data['count']

    if count == 1:
        # Генерация данных для первого слайда
        first_slide_data = generate_first_slide(keyword)
        if not first_slide_data:
            return Response({'error': 'Не удалось сгенерировать первый слайд'}, status=400)

        # Сохраняем данные в SlideFirst
        first_slide = SlideFirst(
            keyword=keyword,
            title=first_slide_data["title"],
            description=first_slide_data["description"],
            image_url=first_slide_data["image_url"]
        )
        first_slide.save()

        # Сериализуем данные для ответа
        serializer = SlideFirstSerializer(first_slide)
        return Response({"first_slide": serializer.data}, status=status.HTTP_200_OK)

    elif count == 2:
        # Генерация данных для первого и второго слайдов
        first_slide_data = generate_first_slide(keyword)
        second_slide_data = generate_second_slide(keyword)

        if not first_slide_data or not second_slide_data:
            return Response({'error': 'Не удалось сгенерировать слайды'}, status=400)

        # Сохраняем первый слайд в SlideFirst
        first_slide = SlideFirst(
            keyword=keyword,
            title=first_slide_data["title"],
            description=first_slide_data["description"],
            image_url=first_slide_data["image_url"]
        )
        first_slide.save()

        # Сохраняем второй слайд в Slide
        second_slide = Slide(
            keyword=keyword,
            title=second_slide_data["title"],
            subtitle_1=second_slide_data["subtitle_1"],
            description_1=second_slide_data["description_1"],
            subtitle_2=second_slide_data["subtitle_2"],
            description_2=second_slide_data["description_2"],
            subtitle_3=second_slide_data["subtitle_3"],
            description_3=second_slide_data["description_3"],
            subtitle_4=second_slide_data["subtitle_4"],
            description_4=second_slide_data["description_4"],
            image_url=second_slide_data["image_url"]
        )
        second_slide.save()

        # Сериализуем данные для ответа
        first_serializer = SlideFirstSerializer(first_slide)
        second_serializer = SlideSerializer(second_slide)
        return Response({
            "id": first_slide.id,
            "first_slide": first_serializer.data,
            "second_slide": second_serializer.data
        }, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Некорректное значение count'}, status=status.HTTP_400_BAD_REQUEST)


class GetLastSlideAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Получаем последний SlideFirst
        last_slide_first = SlideFirst.objects.last()
        if not last_slide_first:
            return Response({'error': 'Нет данных'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем связанный Slide (если есть)
        last_slide = Slide.objects.filter(id=last_slide_first.id).first()

        # Сериализуем данные
        first_serializer = SlideFirstSerializer(last_slide_first)
        response_data = {
            "id": last_slide_first.id,
            "first_slide": first_serializer.data
        }

        if last_slide:
            second_serializer = SlideSerializer(last_slide)
            response_data["second_slide"] = second_serializer.data

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_answers(request):
    # Получаем все объекты Slide из базы данных
    slides = Slide.objects.all()

    # Сериализуем данные
    serializer = SlideSerializer(slides, many=True)

    # Возвращаем сериализованные данные
    return Response(serializer.data)


