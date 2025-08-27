from django.db import models

# Create your models here.

class Message(models.Model):
    identifier = models.CharField(max_length=50)
    password = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.identifier} ({self.created_at:%Y-%m-%d %H:%M})"