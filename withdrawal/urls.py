from django.urls import path
from .views import *

urlpatterns = [
    path('', UserWithdrawalAPIView.as_view(), name='user_withdrawal'),
    path('local_bank/', LocalBankWithdrawalAPIView.as_view(), name='local_bank_withdrawal_create'),
    path('<int:pk>/verify/', WithdrawalVerificationAPIView.as_view(), name='withdrawal-verification'),
    path('user/withdrawals', UserWithdrawalListView.as_view(), name='user_withdrawal_list'),
    path('approved/', ApprovedWithdrawalListView.as_view(), name='approved_withdrawal_list'),
    path('pending/', PendingWithdrawalListView.as_view(), name='pending_withdrawal_list'),
    path('<int:pk>/', WithdrawalDeleteView.as_view(), name='withdrawal_delete'),
    path('list/all/', AllWithdrawalListView.as_view(), name='all_withdrawal_list')
]
