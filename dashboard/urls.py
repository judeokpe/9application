from django.urls import path
from .views import *

urlpatterns = [
    path('user_list/', UserListView.as_view(), name='user_lists'),
    path('total_users/', TotalUsersAPIView.as_view(), name='total_users'),
    path('deposit_list/', DepositListView.as_view(), name='depsoit_lists'),
    path('total_deposits/', TotalDepositsAPIView.as_view(), name='total_deposits'),
    path('withdrawal_list/', WithdrawalListView.as_view(), name='withdrawal_lists'),
    path('total_withdrawals/', TotalWithdrawalsAPIView.as_view(), name='total_withdrawals'),
    path('verified_deposits/', VerifiedDepositsAPIView.as_view(), name='verified_deposits'),
    path('pending_deposits/', PendingDepositsAPIView.as_view(), name='pending_deposits'),
    path('verified_withdrawals/', VerifiedWithdrawalsAPIView.as_view(), name='verified_withdrawals'),
    path('pending_withdrawals/', PendingWithdrawalsAPIView.as_view(), name='pending_withdrawals'),
    path('pending_withdrawals_list/', PendingWithdrawalsView.as_view(), name='pending_withdrawals_list'),
    path('verified_withdrawals_list/', VerifiedWithdrawalsView.as_view(), name='pending_withdrawals_list'),
    path('pending_deposit_list/', PendingDepositsView.as_view(), name='pending_deposits_list'),
    path('verified_deposit_list/', VerifiedDepositsView.as_view(), name='verified_deposits_list'),
    path('user/', UserDashboardAPIView.as_view(), name='user_dashboard'),
    path('user/activities/', ActivityListAPIView.as_view(), name='activity_list'),

]
