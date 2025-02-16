# from channels.generic.websocket import AsyncWebsocketConsumer
# import asyncio
# import json
# import httpx
# from asgiref.sync import sync_to_async
# from django.apps import apps
#
# API_URL = "https://8d2f-92-62-69-226.ngrok-free.app/ask_stream"
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.BotResponse = apps.get_model('my_app', 'BotResponse')
#         from .serializers import MessageSerializer
#         self.MessageSerializer = MessageSerializer
#         self.queue = asyncio.Queue(maxsize=1000)  # Ограничение на 1000 запросов в очереди
#         self.processing = False
#
#     async def connect(self):
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         pass
#
#     async def receive(self, text_data):
#         # Проверяем, заполнена ли очередь
#         if self.queue.full():
#             await self.send(text_data=json.dumps({
#                 "error": "Сервер занят, отправьте запрос позже",
#             }, ensure_ascii=False))
#             return
#
#         # Добавляем запрос в очередь
#         await self.queue.put(text_data)
#
#         # Если обработка ещё не запущена, запускаем её
#         if not self.processing:
#             await self.process_queue()
#
#     async def process_queue(self):
#         self.processing = True
#         while not self.queue.empty():
#             # Получаем следующий запрос из очереди
#             text_data = await self.queue.get()
#
#             # Обрабатываем запрос
#             text_data_json = json.loads(text_data)
#             message = text_data_json.get("message")
#
#             serializer = self.MessageSerializer(data={"message": message})
#             if serializer.is_valid():
#                 payload = {"prompt": message}
#                 headers = {"Accept": "text/event-stream"}
#
#                 async with httpx.AsyncClient() as client:
#                     try:
#                         response = await client.post(API_URL, json=payload, headers=headers, timeout=None)
#
#                         response_data = ""
#                         async for line in response.aiter_lines():
#                             decoded_line = line.strip()
#                             if decoded_line.startswith("data: "):
#                                 chunk = decoded_line.replace("data: ", "")
#                                 if chunk == "[DONE]":
#                                     break
#                                 response_data += chunk
#                                 await self.send(text_data=json.dumps({
#                                     "status": "Частичный ответ",
#                                     "response": response_data,
#                                 }, ensure_ascii=False))
#
#                         response_data = response_data.strip()
#
#                         if not response_data:
#                             response_data = "Ошибка: пустой ответ от сервера"
#
#                         await sync_to_async(self.BotResponse.objects.create)(
#                             message=message, response=response_data
#                         )
#
#                         await self.send(text_data=json.dumps({
#                             "status": "Сообщение полностью получено!",
#                             "response": response_data,
#                         }, ensure_ascii=False))
#
#                     except httpx.TimeoutException:
#                         await self.send(text_data=json.dumps({
#                             "error": "Ошибка: превышено время ожидания запроса",
#                         }, ensure_ascii=False))
#                     except httpx.HTTPStatusError as e:
#                         await self.send(text_data=json.dumps({
#                             "error": f"Ошибка HTTP: {e.response.status_code}",
#                         }, ensure_ascii=False))
#                     except httpx.RequestError as e:
#                         await self.send(text_data=json.dumps({
#                             "error": f"Ошибка запроса к API: {str(e)}",
#                         }, ensure_ascii=False))
#             else:
#                 await self.send(text_data=json.dumps({
#                     "error": serializer.errors,
#                 }, ensure_ascii=False))
#
#             # Помечаем запрос как выполненный
#             self.queue.task_done()
#
#         self.processing = False
#


# ОТПРАВИТ ТЕКСТ ПО КУСКАМ
#
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import httpx
# from asgiref.sync import sync_to_async
# from django.apps import apps
#
# API_URL = "https://https://8d2f-92-62-69-226.ngrok-free.app"
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


#
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import httpx
# from asgiref.sync import sync_to_async
# from django.apps import apps
#
# API_URL = "https://8d2f-92-62-69-226.ngrok-free.app/ask_stream"
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
#                             response_data += chunk
#                             await self.send(text_data=json.dumps({
#                                 "status": "Частичный ответ",
#                                 "response": response_data,
#                             }, ensure_ascii=False))
#
#                     response_data = response_data.strip()
#
#                     if not response_data:
#                         response_data = "Ошибка: пустой ответ от сервера"
#
#                     await sync_to_async(self.BotResponse.objects.create)(
#                         message=message, response=response_data
#                     )
#
#                     await self.send(text_data=json.dumps({
#                         "status": "Сообщение полностью получено!",
#                         "response": response_data,
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
#

from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json
import httpx
from asgiref.sync import sync_to_async
from django.apps import apps

API_URL = "https://e5bf-217-29-24-178.ngrok-free.app"

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BotResponse = apps.get_model('my_app', 'BotResponse')
        from .serializers import MessageSerializer
        self.MessageSerializer = MessageSerializer
        self.queue = asyncio.Queue(maxsize=1000)  # Ограничение на 1000 запросов в очереди
        self.processing = False

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Проверяем, заполнена ли очередь
        if self.queue.full():
            await self.send(text_data=json.dumps({
                "error": "Сервер занят, отправьте запрос позже",
            }, ensure_ascii=False))
            return

        # Добавляем запрос в очередь
        await self.queue.put(text_data)

        # Если обработка ещё не запущена, запускаем её
        if not self.processing:
            await self.process_queue()

    async def process_queue(self):
        self.processing = True
        while not self.queue.empty():
            # Получаем следующий запрос из очереди
            text_data = await self.queue.get()

            # Обрабатываем запрос
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")

            serializer = self.MessageSerializer(data={"message": message})
            if serializer.is_valid():
                payload = {
                    "model": "Qwen/Qwen2.5-3B-Instruct",  # Используем правильную модель
                    "messages": [
                        {"role": "user", "content": message}  # Вставляем сообщение пользователя
                    ],
                    "stream": True  # Устанавливаем флаг stream, если это необходимо
                }
                headers = {"Content-Type": "application/json"}

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
                                # Добавляем контент из каждого чанка в общий ответ
                                try:
                                    chunk_data = json.loads(chunk)
                                    content = chunk_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                    if content:
                                        response_data += content  # Накопление текста
                                except json.JSONDecodeError:
                                    pass  # Если данные не удается распарсить, игнорируем

                        if not response_data:
                            response_data = "Ошибка: пустой ответ от сервера"

                        # Сохраняем ответ в БД
                        await sync_to_async(self.BotResponse.objects.create)(
                            message=message, response=response_data
                        )

                        # Отправляем только финальный ответ
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

            # Помечаем запрос как выполненный
            self.queue.task_done()

        self.processing = False

