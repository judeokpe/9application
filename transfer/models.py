from django.db import models
from common.models import BaseModel
from account.models import CustomUser
# Create your models here.

class Transfer(BaseModel):
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient_address = models.CharField(max_length=200)
    currency = models.CharField(max_length=5)
    naira_amount = models.DecimalField(max_digits=20, decimal_places=5, default=0.0)  # Equivalent amount in NGN
