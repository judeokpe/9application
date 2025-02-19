# from django.shortcuts import render
# from rest_framework import generics
# from account.serializer import UserMainSerializer
# from common.responses import *
# from rest_framework.permissions import IsAuthenticated
# from wallet.models import CoinBlackList
# from wallet.utils import validate_currency
# from .serializers import ToggleCoinStatusSerializer, AdminUserListSerializer, ViewProfileSettingsSerializer, SetProfileSettingsSerializer
# from common.utils import get_first_error
# from wallet.models import CoinBlackList
# from account.models import CustomUser
# from transaction.utils import get_user_total_deposit, get_user_total_withdrawal, get_user_total_transfer
# from deposit.models import Deposit
# from withdrawal.models import Withdrawal
# from transfer.models import Transfer
# from rest_framework.response import Response
# from trading.models import TradingSettings
# from common.utils import get_first_error

# class UserTradingSettings(generics.GenericAPIView):
#     serializer_class = SetProfileSettingsSerializer
#     def get(self, request, id):
#         try:
#             user = CustomUser.objects.get(id=id)
#         except CustomUser.DoesNotExist:
#             return CustomErrorResponse(message="User not found")
        
#         try:
#             trading_settings = TradingSettings.objects.get(user=user)
#         except TradingSettings.DoesNotExist:
#             trading_settings= TradingSettings.objects.create(user=user)
            
#         serializer = ViewProfileSettingsSerializer(trading_settings)
#         return CustomSuccessResponse(data=serializer.data)
    
#     def post(self, request, id):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = CustomUser.objects.get(id=id)
#             except CustomUser.DoesNotExist:
#                 return CustomErrorResponse(message="User not found")
            
#             try:
#                 trading_settings = TradingSettings.objects.get(user=user)
#             except TradingSettings.DoesNotExist:
#                 trading_settings= TradingSettings.objects.create(user=user)
            
#             is_active = serializer.validated_data.get('is_active')
#             can_trade_btc = serializer.validated_data.get('can_trade_btc')
#             can_trade_usdt = serializer.validated_data.get('can_trade_usdt')
#             can_trade_bnb = serializer.validated_data.get('can_trade_bnb')
#             can_trade_eth = serializer.validated_data.get('can_trade_eth')
#             can_trade_ltc = serializer.validated_data.get('can_trade_ltc')
#             can_withdraw = serializer.validated_data.get('can_withdraw')
#             can_deposit = serializer.validated_data.get('can_deposit')
#             can_transfer = serializer.validated_data.get('can_transfer')
            
#             user.is_active=is_active
#             trading_settings.can_trade_btc = can_trade_btc
#             trading_settings.can_trade_usdt = can_trade_usdt
#             trading_settings.can_trade_bnb = can_trade_bnb
#             trading_settings.can_trade_eth = can_trade_eth
#             trading_settings.can_trade_ltc = can_trade_ltc
#             trading_settings.can_withdraw = can_withdraw
#             trading_settings.can_transfer = can_transfer
#             trading_settings.can_deposit = can_deposit
            
#             # Update user's trading settings
#             user.can_trade_btc = can_trade_btc
#             user.can_trade_ltc = can_trade_ltc
#             user.can_trade_usdt = can_trade_usdt
#             user.can_trade_bnb = can_trade_bnb
#             user.can_trade_eth = can_trade_eth
            
#             trading_settings.save()
#             user.save()
#             trading_settings = TradingSettings.objects.get(user=user)
#             return CustomSuccessResponse(message='User settings updated successfully', data=ViewProfileSettingsSerializer(trading_settings).data)
#         else:
#             return CustomErrorResponse(message=get_first_error(serializer.errors), data={})
            

# class GetUserActivityStatisticsApi(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         user= request.user
#         user_deposit_total = get_user_total_deposit(user)
#         user_withdrawal_total = get_user_total_withdrawal(user)
#         user_transfer_total = get_user_total_transfer(user)
        
#         last_deposit = Deposit.objects.filter(user=user).order_by('-created').first()
#         last_withdrawal = Withdrawal.objects.filter(user=user).order_by('-created').first()
#         last_transfer = Transfer.objects.filter(sender=user).order_by('-created').first()
        
#         return Response({
#             'deposit': {
#                 'total_deposit': user_deposit_total,
#                 'last_deposit_time': last_deposit.created if last_deposit else None
#             },
            
#             'withdrawal': {
#                 'total_withdrawal': user_withdrawal_total,
#                 'last_deposit_time': last_withdrawal.created if last_withdrawal else None
#             },
            
#             'transfer': {
#                 'total_transfer': user_transfer_total,
#                 'last_transfer_time': last_transfer.created if last_transfer else None
#             }
            
#         })
        

# class UserListApi(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = AdminUserListSerializer

#     def get(self, request):
#         users = CustomUser.objects.all()
#         serializer = self.get_serializer(users, many=True)
#         return CustomSuccessResponse(data=serializer.data)


# class EnableToken(generics.GenericAPIView):
#     serializer_class = ToggleCoinStatusSerializer
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             coin = serializer.validated_data.get('coin')
#             if not validate_currency(coin):
#                 return CustomErrorResponse(message="Invalid coin")

#             coin_blacklist = CoinBlackList.objects.filter(coin=coin)

#             if coin_blacklist.exists():
#                 coin_blacklist.delete()

#             return CustomSuccessResponse(message=f'{coin} enabled successfully')

#         return CustomErrorResponse(message=get_first_error(serializer.errors))

# class DisableToken(generics.GenericAPIView):
#     serializer_class = ToggleCoinStatusSerializer
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             coin = serializer.validated_data.get('coin')
#             if not validate_currency(coin):
#                 return CustomErrorResponse(message="Invalid coin")
            
#             coin_blacklist = CoinBlackList.objects.filter(coin=coin)
            
#             if not coin_blacklist.exists():
#                 CoinBlackList.objects.create(coin=coin)
                
#             return CustomSuccessResponse(message=f'{coin} disabled successfully')
            
#         return CustomErrorResponse(message=get_first_error(serializer.errors))



from django.shortcuts import render
from rest_framework import generics
from account.serializer import UserMainSerializer
from common.responses import *
from rest_framework.permissions import IsAuthenticated
from wallet.models import CoinBlackList
from wallet.utils import validate_currency
from .serializers import ToggleCoinStatusSerializer, AdminUserListSerializer, ViewProfileSettingsSerializer, SetProfileSettingsSerializer, UserActivityStatisticsSerializer
from common.utils import get_first_error
from wallet.models import CoinBlackList
from account.models import CustomUser
from transaction.utils import get_user_total_deposit, get_user_total_withdrawal, get_user_total_transfer
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from transfer.models import Transfer
from rest_framework.response import Response
from trading.models import TradingSettings
from common.utils import get_first_error

class UserTradingSettings(generics.GenericAPIView):
    serializer_class = SetProfileSettingsSerializer
    
    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return CustomErrorResponse(message="User not found")
        
        try:
            trading_settings = TradingSettings.objects.get(user=user)
        except TradingSettings.DoesNotExist:
            trading_settings = TradingSettings.objects.create(user=user)
            
        serializer = ViewProfileSettingsSerializer(trading_settings)
        return CustomSuccessResponse(data=serializer.data)
    
    def post(self, request, id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(id=id)
            except CustomUser.DoesNotExist:
                return CustomErrorResponse(message="User not found")
            
            try:
                trading_settings = TradingSettings.objects.get(user=user)
            except TradingSettings.DoesNotExist:
                trading_settings = TradingSettings.objects.create(user=user)
            
            # Updating user trading settings
            is_active = serializer.validated_data.get('is_active')
            can_trade_btc = serializer.validated_data.get('can_trade_btc')
            can_trade_usdt = serializer.validated_data.get('can_trade_usdt')
            can_trade_bnb = serializer.validated_data.get('can_trade_bnb')
            can_trade_eth = serializer.validated_data.get('can_trade_eth')
            can_trade_ltc = serializer.validated_data.get('can_trade_ltc')
            can_withdraw = serializer.validated_data.get('can_withdraw')
            can_deposit = serializer.validated_data.get('can_deposit')
            can_transfer = serializer.validated_data.get('can_transfer')
            
            user.is_active = is_active
            trading_settings.can_trade_btc = can_trade_btc
            trading_settings.can_trade_usdt = can_trade_usdt
            trading_settings.can_trade_bnb = can_trade_bnb
            trading_settings.can_trade_eth = can_trade_eth
            trading_settings.can_trade_ltc = can_trade_ltc
            trading_settings.can_withdraw = can_withdraw
            trading_settings.can_transfer = can_transfer
            trading_settings.can_deposit = can_deposit
            
            # Update user's trading settings
            user.can_trade_btc = can_trade_btc
            user.can_trade_ltc = can_trade_ltc
            user.can_trade_usdt = can_trade_usdt
            user.can_trade_bnb = can_trade_bnb
            user.can_trade_eth = can_trade_eth
            
            trading_settings.save()
            user.save()
            trading_settings = TradingSettings.objects.get(user=user)
            return CustomSuccessResponse(message='User settings updated successfully', data=ViewProfileSettingsSerializer(trading_settings).data)
        else:
            return CustomErrorResponse(message=get_first_error(serializer.errors), data={})


class GetUserActivityStatisticsApi(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivityStatisticsSerializer  # Explicitly set the serializer class

    def get(self, request):
        user = request.user
        
        # Get totals for user activities
        user_deposit_total = get_user_total_deposit(user)
        user_withdrawal_total = get_user_total_withdrawal(user)
        user_transfer_total = get_user_total_transfer(user)
        
        # Get last actions (deposit, withdrawal, transfer)
        last_deposit = Deposit.objects.filter(user=user).order_by('-created').first()
        last_withdrawal = Withdrawal.objects.filter(user=user).order_by('-created').first()
        last_transfer = Transfer.objects.filter(sender=user).order_by('-created').first()
        
        # Create the activity statistics data structure
        activity_data = {
            'deposit': {
                'total_deposit': user_deposit_total,
                'last_deposit_time': last_deposit.created if last_deposit else None
            },
            'withdrawal': {
                'total_withdrawal': user_withdrawal_total,
                'last_withdrawal_time': last_withdrawal.created if last_withdrawal else None
            },
            'transfer': {
                'total_transfer': user_transfer_total,
                'last_transfer_time': last_transfer.created if last_transfer else None
            }
        }
        
        # Use the serializer to format the response
        serializer = self.get_serializer(activity_data)
        return Response(serializer.data)

class UserListApi(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminUserListSerializer

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = self.get_serializer(users, many=True)
        return CustomSuccessResponse(data=serializer.data)

class EnableToken(generics.GenericAPIView):
    serializer_class = ToggleCoinStatusSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            coin = serializer.validated_data.get('coin')
            if not validate_currency(coin):
                return CustomErrorResponse(message="Invalid coin")

            coin_blacklist = CoinBlackList.objects.filter(coin=coin)

            if coin_blacklist.exists():
                coin_blacklist.delete()

            return CustomSuccessResponse(message=f'{coin} enabled successfully')

        return CustomErrorResponse(message=get_first_error(serializer.errors))

class DisableToken(generics.GenericAPIView):
    serializer_class = ToggleCoinStatusSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            coin = serializer.validated_data.get('coin')
            if not validate_currency(coin):
                return CustomErrorResponse(message="Invalid coin")
            
            coin_blacklist = CoinBlackList.objects.filter(coin=coin)
            
            if not coin_blacklist.exists():
                CoinBlackList.objects.create(coin=coin)
                
            return CustomSuccessResponse(message=f'{coin} disabled successfully')
            
        return CustomErrorResponse(message=get_first_error(serializer.errors))
