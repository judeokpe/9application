from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from rest_framework import permissions
from django.db.models import Sum
from account.models import CustomUser
from .serializers import *

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer

class TotalUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_users = CustomUser.objects.count()
        data = {'total_users': total_users}
        serializer = TotalUsersSerializer(data)
        return Response(serializer.data)
    


class DepositListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Deposit.objects.all()
    serializer_class = DepositListSerializer

class TotalDepositsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_deposits = Deposit.objects.count()
        total_deposits_amount = Deposit.objects.aggregate(total_amount=Sum('amount'))['total_amount']
        data = {
            'total_deposits': total_deposits,
            'total_deposits_amount': total_deposits_amount
        }
        serializer = TotalDepositsSerializer(data)
        return Response(serializer.data)
    

class WithdrawalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalListSerializer

class TotalWithdrawalsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_withdrawals = Withdrawal.objects.count()
        total_withdrawals_amount = Withdrawal.objects.aggregate(total_amount=Sum('amount'))['total_amount']
        data = {
            'total_withdrawals': total_withdrawals,
            'total_withdrawals_amount': total_withdrawals_amount
        }
        serializer = TotalWithdrawalsSerializer(data)
        return Response(serializer.data)

class VerifiedDepositsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Deposit.objects.filter(verified=True)
    serializer_class = DepositListSerializer

class PendingDepositsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Deposit.objects.filter(verified=False)
    serializer_class = DepositListSerializer


class VerifiedDepositsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_verified_deposits = Deposit.objects.filter(verified=True).count()
        total_verified_deposits_amount = Deposit.objects.filter(verified=True).aggregate(total_amount=Sum('amount'))['total_amount']
        data = {
            'total_verified_deposits': total_verified_deposits,
            'total_verified_deposits_amount': total_verified_deposits_amount
        }
        serializer = VerifiedDepositsSerializer(data)
        return Response(serializer.data)

class PendingDepositsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_pending_deposits = Deposit.objects.filter(verified=False).count()
        total_pending_deposits_amount = Deposit.objects.filter(verified=False).aggregate(total_amount=Sum('amount'))['total_amount']
        data = {
            'total_pending_deposits': total_pending_deposits,
            'total_pending_deposits_amount': total_pending_deposits_amount
        }
        serializer = PendingDepositsSerializer(data)
        return Response(serializer.data)

class VerifiedWithdrawalsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Withdrawal.objects.filter(verified=True)
    serializer_class = WithdrawalListSerializer

class PendingWithdrawalsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Withdrawal.objects.filter(verified=False)
    serializer_class = WithdrawalListSerializer

class VerifiedWithdrawalsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_verified_withdrawals = Withdrawal.objects.filter(verified=True).count()
        total_verified_withdrawals_amount = Withdrawal.objects.filter(verified=True).aggregate(total_amount=Sum('amount'))['total_amount']
        data = {
            'total_verified_withdrawals': total_verified_withdrawals,
            'total_verified_withdrawals_amount': total_verified_withdrawals_amount
        }
        serializer = VerifiedWithdrawalsSerializer(data)
        return Response(serializer.data)

class PendingWithdrawalsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_pending_withdrawals = Withdrawal.objects.filter(verified=False).count()
        total_pending_withdrawals_amount = Withdrawal.objects.filter(verified=False).aggregate(total_amount=Sum('amount'))['total_amount']
        data = {
            'total_pending_withdrawals': total_pending_withdrawals,
            'total_pending_withdrawals_amount': total_pending_withdrawals_amount
        }
        serializer = PendingWithdrawalsSerializer(data)
        return Response(serializer.data)


# User Dashboard API's
    
class ActivityListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user

        deposits = Deposit.objects.filter(user=user)
        withdrawals = Withdrawal.objects.filter(user=user)

        activities = []
        for deposit in deposits:
            activities.append({'deposit': deposit})
        for withdrawal in withdrawals:
            activities.append({'withdrawal': withdrawal})

        return activities

class UserDashboardAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDashboardSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)