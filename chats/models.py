from django.db import models
from django.conf import settings
from pets.models import Mascota

User = settings.AUTH_USER_MODEL

class Conversation(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name="conversaciones")
    adoptante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_como_adoptante")
    publicador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_como_publicador")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mascota", "adoptante")

    def __str__(self):
        return f"{self.adoptante} ↔ {self.publicador} ({self.mascota.nombre})"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="mensajes")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
