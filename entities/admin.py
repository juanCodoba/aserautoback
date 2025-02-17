# entities/admin.py
from django.contrib import admin
from entities.models import UserMessage

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ("text", "language", "intent", "created_at")
    search_fields = ("text",)