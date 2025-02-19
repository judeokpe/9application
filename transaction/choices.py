from django.db import models

class TRANSACTION_TYPE_CHOICES(models.TextChoices):
    DEPOSIT = 'DEPOSIT', 'Deposit'
    WITHDRAWAL = 'WITHDRAWAL', 'Withdrawal'
    TRANSFER = 'TRANSFER', 'Transfer'