from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from common.responses import *
from trading.models import TradingSettings
from .models import Withdrawal
from .serializers import LocalBankWithdrawalSerializer, WithdrawalSerializer, WithdrawalVerificationSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from account.models import CustomUser


class UserWithdrawalAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawalSerializer

    def perform_create(self, serializer):
        # Set the user field of the withdrawal to the authenticated user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from the serializer
        wallet_address = serializer.validated_data.get('wallet_address')
        amount = serializer.validated_data.get('amount')
        wallet_type = serializer.validated_data.get('wallet_type')

        # Get the trading settings for the authenticated user
        trading_settings = TradingSettings.objects.filter(user=self.request.user).first()

        # Check if the wallet address is provided
        if not wallet_address:
            raise CustomErrorResponse(data={"error": "Wallet address is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is allowed to withdraw the specified coin
        if trading_settings is not None:
            if wallet_type == 'BTC' and not trading_settings.can_trade_btc:
                raise CustomErrorResponse(data={"error": "You are not authorized to withdraw Bitcoin (BTC)."}, status=status.HTTP_403_FORBIDDEN)
            elif wallet_type == 'LTC' and not trading_settings.can_trade_ltc:
                raise CustomErrorResponse(data={"error": "You are not authorized to withdraw Litecoin (LTC)."}, status=status.HTTP_403_FORBIDDEN)
            elif wallet_type == 'USDT' and not trading_settings.can_trade_usdt:
                raise CustomErrorResponse(data={"error": "You are not authorized to withdraw Tether (USDT)."}, status=status.HTTP_403_FORBIDDEN)
            elif wallet_type == 'BNB' and not trading_settings.can_trade_bnb:
                raise CustomErrorResponse(data={"error": "You are not authorized to withdraw Binance (BNB)."}, status=status.HTTP_403_FORBIDDEN)
            elif wallet_type == 'ETH' and not trading_settings.can_trade_eth:
                raise CustomErrorResponse(data={"error": "You are not authorized to withdraw Ethereum (ETH)."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user has sufficient funds for the withdrawal
        if self.request.user.available_balance < amount:
            raise CustomErrorResponse(data={"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        withdrawal = serializer.instance

        try:
            # Send email to the user
            user_email_subject = 'Withdrawal Request Received'
            user_email_message = f'Your withdrawal request of {withdrawal.amount} {withdrawal.get_wallet_type_display()} has been received.'
            send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [request.user.email])

        except Exception as e:
            print(e)

        headers = self.get_success_headers(serializer.data)
        return CustomSuccessResponse(serializer.data, message="Withdrawal request created successfully", status=status.HTTP_201_CREATED, headers=headers)


class LocalBankWithdrawalAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocalBankWithdrawalSerializer

    def perform_create(self, serializer):
        # Set the user field of the withdrawal to the authenticated user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from the serializer
        amount = serializer.validated_data.get('naira_amount')

        # Get the trading settings for the authenticated user
        trading_settings = TradingSettings.objects.filter(user=self.request.user).first()

        # Check if the user is allowed to withdraw
        if trading_settings is not None:
            if not trading_settings.can_withdraw:
                return CustomErrorResponse404(data={"error": "Withdrawal not allowed for this user."})

        print("User's available balance:", self.request.user.available_balance)
        print("Withdrawal amount (NGN):", amount)

        # Check if the user has sufficient funds for the withdrawal
        if self.request.user.available_balance < amount:
            raise ValidationError("Insufficient funds.")

        self.perform_create(serializer)
        
        withdrawal = serializer.instance

        try:
            # Send email to the user
            user_email_subject = 'Withdrawal Request Received'
            user_email_message = f'Your withdrawal request of {amount} NGN has been received.'
            send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [request.user.email])

        except Exception as e:
            print(e)

        return CustomSuccessResponse(data=serializer.data, message="Withdrawal request successful.", status=status.HTTP_201_CREATED)



class WithdrawalVerificationAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            withdrawal = Withdrawal.objects.get(pk=pk)
        except Withdrawal.DoesNotExist:
            return CustomErrorResponse(data={"error": "Withdrawal not found."}, status=404)

        serializer = WithdrawalVerificationSerializer(instance=withdrawal, data={'verified': True}, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Send email notification to the user
            user_email_subject = 'Withdrawal Verified'
            user_email_message = f'Your withdrawal has been verified.'
            send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [withdrawal.user.email])

            return CustomSuccessResponse(data=serializer.data, message="Withdrawal verified successfully")
        else:
            return CustomErrorResponse(data=serializer.errors, status=400)
        


class AllWithdrawalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawalSerializer
    queryset = Withdrawal.objects.all()

class UserWithdrawalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            queryset = Withdrawal.objects.filter(user=user)
            return queryset
        except Withdrawal.DoesNotExist:
            return CustomErrorResponse(data={"error": "No withdrawals found for this user."}, status=404)


class ApprovedWithdrawalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        try:
            queryset = Withdrawal.objects.filter(verified=True)
            return queryset
        except Withdrawal.DoesNotExist:
            return CustomErrorResponse(data={"error": "No approved withdrawals found."}, status=404)


class PendingWithdrawalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        queryset = Withdrawal.objects.filter(verified=False)
        if not queryset.exists():
            raise CustomErrorResponse404(data={"error": "No pending withdrawals found."})
        return queryset

class WithdrawalDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        withdrawal = get_object_or_404(Withdrawal, pk=pk, user=request.user)
        withdrawal.delete()
        return CustomErrorResponse204(message="Withdrawal deleted successfully.")