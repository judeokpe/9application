from django.db import models
from account.models import CustomUser
from common.models import BaseModel 
from decimal import Decimal
from account.utils import send_activation_email

class Deposit(BaseModel):  
    WALLET_TYPE_CHOICES = (
        ('BTC', 'Bitcoin'),
        ('LTC', 'Litecoin'),
        ('USDT', 'Tether'),
        ('BNB', 'Binance'),
        ('ETH', 'Ethereum'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    wallet_type = models.CharField(choices=WALLET_TYPE_CHOICES, max_length=10)
    wallet_address = models.CharField(max_length=100)
    naira_amount = models.DecimalField(max_digits=20, decimal_places=5, default=0.0)  # Equivalent amount in NGN
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Deposit of {self.amount} {self.get_wallet_type_display()} ({self.naira_amount} NGN) to {self.wallet_address}'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Update user's available balance with NGN amount
            self.user.available_balance += Decimal(self.naira_amount)  # Convert to Decimal
            self.user.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.available_balance -= Decimal(self.naira_amount)  # Deduct NGN amount from user's available balance
        self.user.save()
        super().delete(*args, **kwargs)
