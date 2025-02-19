# from rest_framework import serializers
# from account.models import CustomUser
# from wallet.utils import get_user_balance
# from account.serializer import UserMainSerializer
# from trading.models import TradingSettings


# class ViewProfileSettingsSerializer(serializers.ModelSerializer):
#     user = UserMainSerializer()
#     is_active = serializers.SerializerMethodField()
#     class Meta:
#         model = TradingSettings
#         fields = ['user', 'is_active', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth']
#         read_only_fields = ['user']
    
#     def get_is_active(self, obj):
#         return obj.user.is_active

# class AdminTradingSettingsSerializer(serializers.ModelSerializer):
#     is_active = serializers.BooleanField(default=True)
#     class Meta:
#         model = TradingSettings
#         fields = ['is_active', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth', 'can_deposit', 'can_transfer', 'can_withdraw']
        
        
# class SetProfileSettingsSerializer(serializers.Serializer):
#     is_active = serializers.BooleanField(required=True)
#     can_trade_btc = serializers.BooleanField(required=True)
#     can_trade_usdt = serializers.BooleanField(required=True)
#     can_trade_bnb = serializers.BooleanField(required=True)
#     can_trade_eth = serializers.BooleanField(required=True)
#     can_trade_ltc = serializers.BooleanField(required=True)
#     can_withdraw = serializers.BooleanField(required=True)
#     can_deposit = serializers.BooleanField(required=True)
#     can_transfer = serializers.BooleanField(required=True)
    
#     class Meta:
#         fields = ['is_active', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth', 'can_withdraw', 'can_deposit', 'can_transfer']
    
    

# class AdminUserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'
    

# class ToggleCoinStatusSerializer(serializers.Serializer):
#     coin = serializers.CharField(max_length=20, required=True)
#     class Meta:
#         fields = ['coin']



from rest_framework import serializers
from account.models import CustomUser
from wallet.utils import get_user_balance
from account.serializer import UserMainSerializer
from trading.models import TradingSettings
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from transfer.models import Transfer
from transaction.utils import get_user_total_deposit, get_user_total_withdrawal, get_user_total_transfer


# Existing serializers

class ViewProfileSettingsSerializer(serializers.ModelSerializer):
    user = UserMainSerializer()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = TradingSettings
        fields = ['user', 'is_active', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth']
        read_only_fields = ['user']
    
    def get_is_active(self, obj):
        return obj.user.is_active


class AdminTradingSettingsSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = TradingSettings
        fields = ['is_active', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth', 'can_deposit', 'can_transfer', 'can_withdraw']
        
        
class SetProfileSettingsSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)
    can_trade_btc = serializers.BooleanField(required=True)
    can_trade_usdt = serializers.BooleanField(required=True)
    can_trade_bnb = serializers.BooleanField(required=True)
    can_trade_eth = serializers.BooleanField(required=True)
    can_trade_ltc = serializers.BooleanField(required=True)
    can_withdraw = serializers.BooleanField(required=True)
    can_deposit = serializers.BooleanField(required=True)
    can_transfer = serializers.BooleanField(required=True)

    class Meta:
        fields = ['is_active', 'can_trade_btc', 'can_trade_ltc', 'can_trade_usdt', 'can_trade_bnb', 'can_trade_eth', 'can_withdraw', 'can_deposit', 'can_transfer']


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ToggleCoinStatusSerializer(serializers.Serializer):
    coin = serializers.CharField(max_length=20, required=True)

    class Meta:
        fields = ['coin']


# **New serializer** to handle user activity statistics (deposit, withdrawal, transfer)

class UserActivityStatisticsSerializer(serializers.Serializer):
    deposit = serializers.DictField(child=serializers.CharField())
    withdrawal = serializers.DictField(child=serializers.CharField())
    transfer = serializers.DictField(child=serializers.CharField())

    # Optionally, you can add custom validation or methods if needed
    # For example, calculating totals or formatting the last action timestamps
