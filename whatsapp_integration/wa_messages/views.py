import os

from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
import requests

from wa_messages.models import WhatsAppMessage

WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
WHATSAPP_API_ACCESS_TOKEN = os.getenv('WHATSAPP_API_ACCESS_TOKEN')
META_API_DOMAIN = os.getenv('META_API_DOMAIN')


# Create your views here.
class SendMessage(APIView):

    def get(self, request):
        pass

    def post(self, request):
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')

        api_url = f"{META_API_DOMAIN}/{WHATSAPP_PHONE_ID}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message,
            }
        }

        headers = {
            "Authorization": f"Bearer {WHATSAPP_API_ACCESS_TOKEN}",
            "Content-Type": "application/json"}

        response = requests.post(api_url, headers=headers, json=payload)

        return JsonResponse(response.json())


class WebhookView(APIView):

    def get(self, request):
        VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFICATION_TOKEN:
            return HttpResponse(challenge, status=200)
        return JsonResponse({'error': 'Invalid verification token'}, status=400)

    def post(self, request):
        data = request.data
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        receiver = value.get('metadata').get('display_phone_number')

        sender = message.get('from')
        timestamp = message.get('timestamp')
        content = message.get('text').get('body')

        WhatsAppMessage.objects.create(sender=sender, receiver=receiver, timestamp=timestamp, content=content,
                                       status='Received')
        return JsonResponse({'error': 'Invalid verification token'}, status=200)
