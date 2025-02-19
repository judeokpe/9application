from django.db import models
from account.models import CustomUser
from common.models import BaseModel

# Create your models here.

class TradingSettings(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    can_trade_btc = models.BooleanField(default=True)
    can_trade_ltc = models.BooleanField(default=True)
    can_trade_usdt = models.BooleanField(default=True)
    can_trade_bnb = models.BooleanField(default=True)
    can_trade_eth = models.BooleanField(default=True)
    can_deposit = models.BooleanField(default=True)
    can_withdraw = models.BooleanField(default=True)
    can_transfer = models.BooleanField(default=True)
