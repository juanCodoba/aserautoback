# entities/models.py
from django.db import models

class UserMessage(models.Model):
    text = models.TextField()
    language = models.CharField(max_length=10, default="es")
    intent = models.CharField(max_length=50, blank=True, null=True)
    entities = models.JSONField(blank=True, null=True)  # Para almacenar entidades como JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text