from django.db import models
from account.models import CustomUser
from common.models import BaseModel

class Withdrawal(BaseModel):
    WALLET_TYPE_CHOICES = (
        ('BTC', 'Bitcoin'),
        ('LTC', 'Litecoin'),
        ('USDT', 'Tether'),
        ('BNB', 'Binance'),
        ('ETH', 'Ethereum'),
        ('LOCAL_BANK', 'Local Bank'), 
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    wallet_type = models.CharField(choices=WALLET_TYPE_CHOICES, max_length=10)
    wallet_address = models.CharField(max_length=100, blank=True, null=True)  
    naira_amount = models.DecimalField(max_digits=20, decimal_places=5)  # Equivalent amount in NGN
    verified = models.BooleanField(default=False)

    # Fields for local bank withdrawal
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Withdrawal of {self.amount} {self.get_wallet_type_display()} ({self.naira_amount} NGN)'

    def save(self, *args, **kwargs):
        if not self.pk:
            print(f"Before deduction: User available_balance: {self.user.available_balance}")
            if self.user is not None and self.user.available_balance is not None:
                print(f"Deducting {self.naira_amount} from User available_balance")
                self.user.available_balance -= self.naira_amount
                print(f"After deduction: User available_balance: {self.user.available_balance}")
                self.user.save()
            else:
                print("User or available_balance is None")

        super().save(*args, **kwargs)



    

    def delete(self, *args, **kwargs):
        self.user.available_balance += self.naira_amount  # Add back NGN amount to user's available balance
        self.user.save()
        super().delete(*args, **kwargs)
