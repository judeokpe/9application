# from django.db import models
# from common.models import BaseModel
# from django.contrib.auth import get_user_model

# User = get_user_model()
# # Create your models here.
# class Wallet(BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bitcoin_address  = models.CharField(max_length=200)
#     solana_address  = models.CharField(max_length=200)
#     tron_address  = models.CharField(max_length=200)
#     etherum_address  = models.CharField(max_length=200)
#     usdt_address  = models.CharField(max_length=200)

#     def __str__(self) -> str:
#         return self.user.email


# class CoinBlackList(models.Model):
#     coin = models.CharField(max_length=20)
# class WalletBalance(BaseModel):
#     pass


from django.db import models
from common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

# Wallet Model
class Wallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bitcoin_address = models.CharField(max_length=200, blank=True, null=True)
    solana_address = models.CharField(max_length=200, blank=True, null=True)
    tron_address = models.CharField(max_length=200, blank=True, null=True)
    ethereum_address = models.CharField(max_length=200, blank=True, null=True)
    usdt_address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Wallet"

# Coin Blacklist (optional to restrict coins)
class CoinBlackList(models.Model):
    coin = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.coin

# Wallet Balance Model (per coin)
class WalletBalance(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="balances")
    coin = models.CharField(max_length=50)  # e.g., Bitcoin, Ethereum
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    fiat_value = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)  # e.g., in USD

    def __str__(self):
        return f"{self.wallet.user.email} - {self.coin}: {self.amount}"
