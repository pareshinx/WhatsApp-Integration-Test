import os
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView
from rest_framework.views import APIView
import requests
from django.contrib import messages

from wa_messages.forms import LoginForm, SendMessageForm
from wa_messages.models import WhatsAppMessage

WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
WHATSAPP_API_ACCESS_TOKEN = os.getenv('WHATSAPP_API_ACCESS_TOKEN')
META_API_DOMAIN = os.getenv('META_API_DOMAIN')
SENDER_PHONE_NUMBER = os.getenv('SENDER_PHONE_NUMBER')


# Create your views here.
class LoginView(FormView):
    """
        Handles user login using a form. Authenticates superusers and redirects them
        to the dashboard. Displays error messages for invalid credentials or access denial.
    """
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """
               Authenticates the user and logs in if they are a superuser.
               Redirects to the dashboard or displays error messages.
        """
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            if user.is_superuser:
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                messages.error(self.request, 'Access denied: You are not a super admin.')
        else:
            messages.error(self.request, 'Invalid email or password.')

        return super().form_invalid(form)


class LogoutView(View):
    """
       Logs out the user and redirects to the login page.
    """

    def get(self, request):
        """
           Logs out the current user and redirects to the login page.
        """
        logout(request)
        return redirect('login')


class WebhookView(APIView):
    """
        API view to handle webhook events for WhatsApp integration.
        Supports GET requests for verification and POST requests for processing incoming messages.
    """

    def get(self, request):
        """
            Verify the webhook by checking the token.

            Returns:
                HttpResponse: The challenge if the token matches.
                JsonResponse: An error if the token does not match.
        """
        VERIFICATION_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN')
        verify_token = VERIFICATION_TOKEN
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if token == verify_token:
            return HttpResponse(challenge, content_type="text/plain", status=200)
        return JsonResponse({"error": "Invalid token"}, status=403)

    def post(self, request):
        """
            Process incoming WhatsApp messages and save them.

            Returns:
                JsonResponse: A success or error message.
        """
        try:
            data = request.data

            entry = data.get('entry', [{}])[0]
            change = entry.get('changes', [{}])[0]
            value = change.get('value', {})
            message = value.get('messages', [{}])[0]

            sender = message.get('from')
            timestamp = int(message.get('timestamp', 0))
            content = message.get('text', {}).get('body', '')
            receiver = value.get('metadata', {}).get('display_phone_number', '')

            timestamp = datetime.fromtimestamp(timestamp)

            WhatsAppMessage.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                timestamp=timestamp,
                status='Received'
            )

            return JsonResponse({"status": "success", "message": "Message processed"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


class SendMessageView(View):
    """
    Handles rendering the send message form and processing the WhatsApp message request.
    """

    def get(self, request):
        """
        Render the send message form.
        """
        form = SendMessageForm()
        return render(request, 'send_message.html', {'form': form, 'result_message': None})

    def post(self, request):
        """
        Process the form submission to send a WhatsApp message.
        """
        form = SendMessageForm(request.POST)
        result_message = None

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']

            # WhatsApp API Endpoint
            api_url = f"{META_API_DOMAIN}/{WHATSAPP_PHONE_ID}/messages"

            # Payload for the API
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }

            # Headers with authorization
            headers = {
                "Authorization": f"Bearer {WHATSAPP_API_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            # Make the API call
            response = requests.post(api_url, json=payload, headers=headers)

            # Check response status
            if response.status_code == 200:
                result_message = f"Message sent successfully to {phone_number}."
                status = 'Sent'
            else:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                result_message = f"Failed to send message to {phone_number}. Error: {error_detail}"
                status = 'Failed'

            # Store the message in the database
            sender = SENDER_PHONE_NUMBER
            timestamp = datetime.now()
            WhatsAppMessage.objects.create(
                sender=sender,
                receiver=phone_number,
                content=message,
                timestamp=timestamp,
                status=status
            )

        return render(request, 'send_message.html', {'form': form, 'result_message': result_message})


class DashboardView(LoginRequiredMixin, View):
    """
    Displays the dashboard with WhatsApp messages.
    """
    login_url = '/login/'

    def get(self, request):
        # Fetch WhatsApp messages from the database
        messages = WhatsAppMessage.objects.all().order_by('-timestamp')

        # Prepare the messages for rendering in the template
        formatted_messages = [
            {
                'sender': message.sender,
                'receiver': message.receiver,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status': message.status,
            }
            for message in messages
        ]

        return render(request, 'dashboard.html', {'messages': formatted_messages})
