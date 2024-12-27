from django.shortcuts import redirect
from django.urls import path

from wa_messages.views import WebhookView, LoginView, LogoutView, DashboardView, SendMessageView

urlpatterns = [
    path('send-message', SendMessageView.as_view(), name='send-message'),
    path('api/webhook/', WebhookView.as_view(), name='webhook'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', lambda request: redirect('dashboard/')),
]
