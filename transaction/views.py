# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .models import Transaction
# from .serializers import TransactionSerializer
# from deposit.models import Deposit
# from withdrawal.models import Withdrawal
# from .utils import get_total_deposit, get_total_withdrawal
# from common.responses import CustomSuccessResponse


# class GetTransactionStatistics(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         total_deposit = get_total_deposit()
#         return CustomSuccessResponse(data={
#             'total_deposit': total_deposit,
#             'total_withdrawal': get_total_withdrawal(),
#             })

# class AllTransactionApiView(generics.ListAPIView):
#     """
#     Get all transactions
    
#     ---
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = TransactionSerializer
#     queryset = Transaction.objects.all()

# class TransactionListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = TransactionSerializer

#     def get_queryset(self):
#         # Retrieve deposit and withdrawal data
#         user = self.request.user
#         deposits = Deposit.objects.filter(user=user)
#         withdrawals = Withdrawal.objects.filter(user=user)

#         # Combine deposit and withdrawal data into a single queryset
#         transactions = []
#         for deposit in deposits:
#             transaction = Transaction(
#                 user=user,
#                 amount=deposit.amount,
#                 transaction_type='DEPOSIT',
#                 status=deposit.verified,
#                 created_at=deposit.created
#             )
#             transaction.deposit = deposit  # Associate the deposit with the transaction
#             transactions.append(transaction)
            
#         for withdrawal in withdrawals:
#             transaction = Transaction(
#                 user=user,
#                 amount=withdrawal.amount,
#                 transaction_type='WITHDRAWAL',
#                 status=withdrawal.verified,
#                 created_at=withdrawal.created
#             )
#             transaction.withdrawal = withdrawal  # Associate the withdrawal with the transaction
#             transactions.append(transaction)

#         return transactions


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Transaction
from .serializers import TransactionSerializer, EmptySerializer
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from .utils import get_total_deposit, get_total_withdrawal
from common.responses import CustomSuccessResponse
from django.db.models import F


class GetTransactionStatistics(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer  # Use EmptySerializer for schema generation

    def get(self, request):
        total_deposit = get_total_deposit()
        total_withdrawal = get_total_withdrawal()
        return CustomSuccessResponse(data={
            'total_deposit': total_deposit,
            'total_withdrawal': total_withdrawal,
        })


class AllTransactionApiView(generics.ListAPIView):
    """
    Get all transactions
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user

        # Annotate deposit and withdrawal querysets with relevant fields
        deposit_qs = Deposit.objects.filter(user=user).annotate(
            transaction_type=F('DEPOSIT'),
            status=F('verified'),
            created_at=F('created')
        )

        withdrawal_qs = Withdrawal.objects.filter(user=user).annotate(
            transaction_type=F('WITHDRAWAL'),
            status=F('verified'),
            created_at=F('created')
        )

        # Combine and order by created date
        combined_qs = deposit_qs.union(withdrawal_qs).order_by('-created_at')
        return combined_qs
