# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import httpx
# from .models import BotResponse
# from .serializers import MessageSerializer
# from asgiref.sync import sync_to_async
#
# API_URL = "https://0663-92-62-69-226.ngrok-free.app/ask_stream"
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Принимаем соединение
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Закрываем соединение
#         await self.close()
#
#     async def receive(self, text_data):
#         # Получаем сообщение от клиента
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get("message")
#
#         # Валидируем сообщение
#         serializer = MessageSerializer(data={"message": message})
#         if serializer.is_valid():
#             # Отправляем сообщение на API вашего напарника
#             payload = {"prompt": message}
#             async with httpx.AsyncClient() as client:
#                 try:
#                     response = await client.post(API_URL, json=payload, timeout=5)
#                     response.raise_for_status()
#                     response_data = response.json().get("answer", "")
#
#                     # Сохраняем сообщение и ответ в базу данных
#                     await sync_to_async(BotResponse.objects.create)(
#                         message=message, response=response_data
#                     )
#
#                     # Отправляем ответ клиенту
#                     await self.send(text_data=json.dumps({
#                         "status": "Message sent!",
#                         "response": response_data,
#                     }))
#                 except httpx.Timeout:
#                     await self.send(text_data=json.dumps({
#                         "error": "API request timed out",
#                     }))
#                 except httpx.RequestError as e:
#                     await self.send(text_data=json.dumps({
#                         "error": f"API request failed: {str(e)}",
#                     }))
#         else:
#             await self.send(text_data=json.dumps({
#                 "error": serializer.errors,
#             }))
#


from channels.generic.websocket import AsyncWebsocketConsumer
import json
import httpx
from asgiref.sync import sync_to_async
from django.apps import apps

API_URL = "https://5358-92-62-69-226.ngrok-free.app"

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BotResponse = apps.get_model('my_app', 'BotResponse')
        from .serializers import MessageSerializer
        self.MessageSerializer = MessageSerializer

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        serializer = self.MessageSerializer(data={"message": message})
        if serializer.is_valid():
            payload = {"prompt": message}
            headers = {"Accept": "text/event-stream"}

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(API_URL, json=payload, headers=headers, timeout=None)

                    response_data = ""
                    async for line in response.aiter_lines():
                        decoded_line = line.strip()
                        if decoded_line.startswith("data: "):
                            chunk = decoded_line.replace("data: ", "")
                            if chunk == "[DONE]":
                                break
                            response_data += chunk
                            await self.send(text_data=json.dumps({
                                "status": "Частичный ответ",
                                "response": response_data,
                            }, ensure_ascii=False))

                    response_data = response_data.strip()

                    if not response_data:
                        response_data = "Ошибка: пустой ответ от сервера"

                    await sync_to_async(self.BotResponse.objects.create)(
                        message=message, response=response_data
                    )

                    await self.send(text_data=json.dumps({
                        "status": "Сообщение полностью получено!",
                        "response": response_data,
                    }, ensure_ascii=False))

                except httpx.TimeoutException:
                    await self.send(text_data=json.dumps({
                        "error": "Ошибка: превышено время ожидания запроса",
                    }, ensure_ascii=False))
                except httpx.HTTPStatusError as e:
                    await self.send(text_data=json.dumps({
                        "error": f"Ошибка HTTP: {e.response.status_code}",
                    }, ensure_ascii=False))
                except httpx.RequestError as e:
                    await self.send(text_data=json.dumps({
                        "error": f"Ошибка запроса к API: {str(e)}",
                    }, ensure_ascii=False))
        else:
            await self.send(text_data=json.dumps({
                "error": serializer.errors,
            }, ensure_ascii=False))


# ОТПРАВИТ ТЕКСТ ПО КУСКАМ

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import httpx
# from asgiref.sync import sync_to_async
# from django.apps import apps
#
# API_URL = "https://0663-92-62-69-226.ngrok-free.app/ask_stream"
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.BotResponse = apps.get_model('my_app', 'BotResponse')
#         from .serializers import MessageSerializer
#         self.MessageSerializer = MessageSerializer
#
#     async def connect(self):
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.close()
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get("message")
#
#         serializer = self.MessageSerializer(data={"message": message})
#         if serializer.is_valid():
#             payload = {"prompt": message}
#             headers = {"Accept": "text/event-stream"}
#
#             async with httpx.AsyncClient() as client:
#                 try:
#                     response = await client.post(API_URL, json=payload, headers=headers, timeout=None)
#
#                     response_data = ""
#                     async for line in response.aiter_lines():
#                         decoded_line = line.strip()
#                         if decoded_line.startswith("data: "):
#                             chunk = decoded_line.replace("data: ", "")
#                             if chunk == "[DONE]":
#                                 break
#                             response_data += chunk + " "
#
#                             await self.send(text_data=json.dumps({
#                                 "status": "Часть сообщения получена",
#                                 "response": chunk.strip(),
#                             }, ensure_ascii=False))
#
#                     if not response_data.strip():
#                         response_data = "Ошибка: пустой ответ от сервера"
#
#                     await sync_to_async(self.BotResponse.objects.create)(
#                         message=message, response=response_data.strip()
#                     )
#
#                     await self.send(text_data=json.dumps({
#                         "status": "Сообщение полностью получено!",
#                         "response": response_data.strip(),
#                     }, ensure_ascii=False))
#
#                 except httpx.TimeoutException:
#                     await self.send(text_data=json.dumps({
#                         "error": "Ошибка: превышено время ожидания запроса",
#                     }, ensure_ascii=False))
#                 except httpx.HTTPStatusError as e:
#                     await self.send(text_data=json.dumps({
#                         "error": f"Ошибка HTTP: {e.response.status_code}",
#                     }, ensure_ascii=False))
#                 except httpx.RequestError as e:
#                     await self.send(text_data=json.dumps({
#                         "error": f"Ошибка запроса к API: {str(e)}",
#                     }, ensure_ascii=False))
#         else:
#             await self.send(text_data=json.dumps({
#                 "error": serializer.errors,
#             }, ensure_ascii=False))
