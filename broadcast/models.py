from django.db import models

# Create your models here.

class Broadcast(models.Model):
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
