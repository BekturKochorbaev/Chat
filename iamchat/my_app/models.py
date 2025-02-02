from django.db import models

class BotResponse(models.Model):
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Время создания записи

    def __str__(self):
        return f"Message: {self.message} - Response: {self.response}"
