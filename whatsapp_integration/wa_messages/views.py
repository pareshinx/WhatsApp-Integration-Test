import os

from django.http.response import JsonResponse
from rest_framework.views import APIView
import requests

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