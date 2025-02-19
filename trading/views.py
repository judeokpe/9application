from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from account.models import CustomUser
from common.responses import CustomSuccessResponse
from trading.models import TradingSettings
from trading.serializers import TradingSettingsSerializer
from rest_framework.exceptions import NotFound

class TradingSettingsAPIView(generics.RetrieveUpdateAPIView):
    queryset = TradingSettings.objects.all()
    serializer_class = TradingSettingsSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.save()
        user = instance.user
        # Update user's trading settings
        user.can_trade_btc = instance.can_trade_btc
        user.can_trade_ltc = instance.can_trade_ltc
        user.can_trade_usdt = instance.can_trade_usdt
        user.can_trade_bnb = instance.can_trade_bnb
        user.can_trade_eth = instance.can_trade_eth
        user.save()

class TradingSettingsCreateAPIView(generics.CreateAPIView):
    queryset = TradingSettings.objects.all()
    serializer_class = TradingSettingsSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        try:
            user = CustomUser.objects.get(pk=user_id)
            serializer.save(user=user)
        except CustomUser.DoesNotExist:
            raise CustomSuccessResponse(data={"error": "User not found."})