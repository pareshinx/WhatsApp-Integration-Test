from django.db import models


# Create your models here.

class WhatsAppMessage(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=[("Sent", "Sent"),
                                                       ("Received", "Received"),
                                                       ("Failed", "Failed"),
                                                       ])

    def __str__(self):
        return self.content