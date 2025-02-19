from rest_framework import serializers
from trading.models import TradingSettings
from account.models import CustomUser

class TradingSettingsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True)

    class Meta:
        model = TradingSettings
        fields = ['user_id', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth']
