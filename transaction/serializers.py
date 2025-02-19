# from rest_framework import serializers
# from .models import Transaction
# from account.serializer import UserMainSerializer


# class TransactionSerializer(serializers.ModelSerializer):
#     status = serializers.SerializerMethodField()
#     user = UserMainSerializer()

#     class Meta:
#         model = Transaction
#         fields = ['id', 'user', 'amount', 'transaction_type', 'status', 'created']

#     def get_status(self, obj):
#         if obj.transaction_type == 'DEPOSIT':
#             if hasattr(obj, 'deposit') and obj.deposit.verified:
#                 return 'APPROVED'
#             else:
#                 return 'PENDING'
#         elif obj.transaction_type == 'WITHDRAWAL':
#             if hasattr(obj, 'withdrawal') and obj.withdrawal.verified:
#                 return 'APPROVED'
#             else:
#                 return 'PENDING'
#         else:
#             return 'UNKNOWN'


from rest_framework import serializers
from .models import Transaction
from account.serializer import UserMainSerializer


class EmptySerializer(serializers.Serializer):
    """A placeholder serializer for schema generation in views that don't require data input.""" 
    pass


class TransactionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    user = UserMainSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'transaction_type', 'status', 'created']

    def get_status(self, obj):
        if obj.transaction_type == 'DEPOSIT':
            if hasattr(obj, 'deposit') and obj.deposit.verified:
                return 'APPROVED'
            else:
                return 'PENDING'
        elif obj.transaction_type == 'WITHDRAWAL':
            if hasattr(obj, 'withdrawal') and obj.withdrawal.verified:
                return 'APPROVED'
            else:
                return 'PENDING'
        else:
            return 'UNKNOWN'

