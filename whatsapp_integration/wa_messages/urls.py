from django.contrib import admin
from django.urls import path

from wa_messages.views import SendMessage, WebhookView

urlpatterns = [
    path('send-message', SendMessage.as_view(), name='send-message'),
    path('api/webhook/', WebhookView.as_view(), name='webhook'),
]
