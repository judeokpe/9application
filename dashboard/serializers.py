from rest_framework import serializers, generics
from account.models import CustomUser
from deposit.models import Deposit
from withdrawal.models import Withdrawal

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


class TotalUsersSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()


class DepositListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'verified', 'created']

class TotalDepositsSerializer(serializers.Serializer):
    total_deposits = serializers.IntegerField()
    total_deposits_amount = serializers.DecimalField(max_digits=20, decimal_places=5)


class WithdrawalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'verified', 'created']

class TotalWithdrawalsSerializer(serializers.Serializer):
    total_withdrawals = serializers.IntegerField()
    total_withdrawals_amount = serializers.DecimalField(max_digits=20, decimal_places=5)

class VerifiedDepositsSerializer(serializers.Serializer):
    total_verified_deposits = serializers.IntegerField()
    total_verified_deposits_amount = serializers.DecimalField(max_digits=20, decimal_places=5)

class PendingDepositsSerializer(serializers.Serializer):
    total_pending_deposits = serializers.IntegerField()
    total_pending_deposits_amount = serializers.DecimalField(max_digits=20, decimal_places=5)

class VerifiedWithdrawalsSerializer(serializers.Serializer):
    total_verified_withdrawals = serializers.IntegerField()
    total_verified_withdrawals_amount = serializers.DecimalField(max_digits=20, decimal_places=5)

class PendingWithdrawalsSerializer(serializers.Serializer):
    total_pending_withdrawals = serializers.IntegerField()
    total_pending_withdrawals_amount = serializers.DecimalField(max_digits=20, decimal_places=5)


class ActivitySerializer(serializers.Serializer):
    deposit = DepositListSerializer(required=False)
    withdrawal = WithdrawalListSerializer(required=False)

class UserDashboardSerializer(serializers.ModelSerializer):
    available_balance = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['available_balance']

    def get_available_balance(self, obj):
        return f"NGN {obj.available_balance:.2f}"