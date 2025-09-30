from django.db import models
import os
import uuid


def upload_to(instance, filename):
    # Генерируем уникальное имя файла
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


class UploadedFile(models.Model):
    file = models.FileField(upload_to=upload_to)
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

    def delete(self, *args, **kwargs):
        # Удаляем физический файл при удалении записи
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)