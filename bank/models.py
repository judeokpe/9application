from django.db import models
from common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class BankInformation(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=200)
    bank_code = models.CharField(max_length=200, null=True, blank=True)
    account_name = models.CharField(max_length=250)
    account_number = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.user.email
   