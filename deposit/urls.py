from django.urls import path
from .views import (
    ApprovedDepositListView,
    DepositDeleteView,
    # DepositVerificationAPIView,
    PendingDepositListView,
    UserDepositAPIView,
    UserDepositListView,
    AllDepositListView
)

urlpatterns = [
    path('user/deposit/', UserDepositListView.as_view(), name='deposits'),
    path('', UserDepositAPIView.as_view(), name='user_deposit'),
    # path('deposit-verification/<int:pk>/', DepositVerificationAPIView.as_view(), name='deposit-verification'),
    path('approved-deposits/', ApprovedDepositListView.as_view(), name='approved-deposits'),
    path('pending-deposits/', PendingDepositListView.as_view(), name='pending-deposits'),
    path('<int:pk>/delete/', DepositDeleteView.as_view(), name='deposit-delete'),
    path('list/all/', AllDepositListView.as_view(), name='deposit-list')

]
