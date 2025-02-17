from django.urls import path
from .views import process_message

urlpatterns = [
    path('process_message/', process_message, name='process_message'),
]