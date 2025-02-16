from django.db import models

class BotResponse(models.Model):
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Время создания записи

    def __str__(self):
        return f"Message: {self.message} - Response: {self.response}"

class Slide(models.Model):
    group_id = models.IntegerField(verbose_name="ID группы", null=True, blank=True)
    keyword = models.CharField(max_length=255, verbose_name="Ключевое слово")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    subtitle_1 = models.CharField(max_length=255, verbose_name="Подзаголовок 1", blank=True, null=True)
    description_1 = models.TextField(verbose_name="Описание 1", blank=True, null=True)
    subtitle_2 = models.CharField(max_length=255, verbose_name="Подзаголовок 2", blank=True, null=True)
    description_2 = models.TextField(verbose_name="Описание 2", blank=True, null=True)
    subtitle_3 = models.CharField(max_length=255, verbose_name="Подзаголовок 3", blank=True, null=True)
    description_3 = models.TextField(verbose_name="Описание 3", blank=True, null=True)
    subtitle_4 = models.CharField(max_length=255, verbose_name="Подзаголовок 4", blank=True, null=True)
    description_4 = models.TextField(verbose_name="Описание 4", blank=True, null=True)
    image_url = models.URLField(verbose_name="URL изображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Slide: {self.keyword} ({self.created_at})"

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"