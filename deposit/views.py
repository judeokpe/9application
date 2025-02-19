from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from common.responses import *
from .models import Deposit
from .serializers import DepositSerializer, DepositListSerializer
from trading.models import TradingSettings


class UserDepositAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositSerializer

    def perform_create(self, serializer):
        # Set the user field of the deposit to the authenticated user
        serializer.save(user=self.request.user, created=timezone.now())
        print("Deposit created:", serializer.instance)

    def create(self, request, *args, **kwargs):
        user = request.user
        trading_settings = TradingSettings.objects.filter(user=user).first()
        
        # If no trading settings exist, allow deposit for any coin
        if trading_settings is None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            deposit = serializer.instance

            try:
                # Send email to the user
                user_email_subject = 'Deposit Request Received'
                user_email_message = f'Your deposit request of {deposit.amount} {deposit.get_wallet_type_display()} has been received.'
                send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [request.user.email])

            except Exception as e:
                print(e)

            headers = self.get_success_headers(serializer.data)
            return CustomSuccessResponse(data=serializer.data, message="Deposit created successfully", headers=headers)
        
        # Otherwise, check if user is allowed to deposit the specific coin
        wallet_type = request.data.get('wallet_type')
        if wallet_type not in ['BTC', 'LTC', 'USDT', 'BNB', 'ETH']:
            return CustomErrorResponse(message="Invalid coin.", status=status.HTTP_400_BAD_REQUEST)

        if wallet_type == 'BTC' and not trading_settings.can_trade_btc:
            return CustomErrorResponse(message="You are not authorized to deposit Bitcoin (BTC).", status=status.HTTP_403_FORBIDDEN)
        elif wallet_type == 'LTC' and not trading_settings.can_trade_ltc:
            return CustomErrorResponse(message="You are not authorized to deposit Litecoin (LTC).", status=status.HTTP_403_FORBIDDEN)
        elif wallet_type == 'USDT' and not trading_settings.can_trade_usdt:
            return CustomErrorResponse(message="You are not authorized to deposit Tether (USDT).", status=status.HTTP_403_FORBIDDEN)
        elif wallet_type == 'BNB' and not trading_settings.can_trade_bnb:
            return CustomErrorResponse(message="You are not authorized to deposit Binance (BNB).", status=status.HTTP_403_FORBIDDEN)
        elif wallet_type == 'ETH' and not trading_settings.can_trade_eth:
            return CustomErrorResponse(message="You are not authorized to deposit Ethereum (ETH).", status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        deposit = serializer.instance

        try:
            # Send email to the user
            user_email_subject = 'Deposit Request Received'
            user_email_message = f'Your deposit request of {deposit.amount} {deposit.get_wallet_type_display()} has been received.'
            send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [request.user.email])

        except Exception as e:
            print(e)

        headers = self.get_success_headers(serializer.data)
        return CustomSuccessResponse(data=serializer.data, message="Deposit created successfully", headers=headers)
    

# class DepositVerificationAPIView(APIView):
#     permission_classes = [IsAdminUser]

#     def put(self, request, pk):
#         deposit = Deposit.objects.get(pk=pk)
#         serializer = DepositVerificationSerializer(instance=deposit, data={'verified': True}, partial=True)
#         if serializer.is_valid():
#             serializer.save()

#             # Send email notification to the user
#             user_email_subject = 'Deposit Verified'
#             user_email_message = f'Your deposit has been verified.'
#             send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [deposit.user.email])

#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AllDepositListView(generics.ListAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositListSerializer
    permission_classes = [IsAuthenticated]

class UserDepositListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return CustomSuccessResponse(data=serializer.data, message="User deposits retrieved successfully")
        except Deposit.DoesNotExist:
            return CustomErrorResponse404(message="No deposits found for the user")

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)
    
    
class ApprovedDepositListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return CustomSuccessResponse(data=serializer.data, message="Approved deposits retrieved successfully")
        except Deposit.DoesNotExist:
            return CustomErrorResponse404(message="No approved deposits found")

    def get_queryset(self):
        return Deposit.objects.filter(verified=True)
    

class PendingDepositListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return CustomSuccessResponse(data=serializer.data, message="Pending deposits retrieved successfully")
        except Deposit.DoesNotExist:
            return CustomErrorResponse404(message="No pending deposits found")

    def get_queryset(self):
        return Deposit.objects.filter(verified=False)


class DepositDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            deposit = Deposit.objects.get(pk=pk)
            deposit.delete()
            return CustomErrorResponse204(message="Deposit deleted successfully")
        except Deposit.DoesNotExist:
            return CustomErrorResponse404(message="Deposit does not exist.")