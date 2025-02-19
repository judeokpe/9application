# # urls.py (Add this to your existing urls file)

# from django.urls import path
# from .views import (GetWalletAddress, GetWalletBalance, TransferCoin, CoinSwap, GetCurrencyPrice,TransactionHistory,CryptocurrencyTransactions,
#                     GetIndividualCurrencyBalance, GetUSDPrice, GetNairaPrice, USDTtoNGN, GetExchangeEstimate, GetSwapStatus, ValidateCurrency, GetNairaEquivalent)

# urlpatterns = [
#     path('wallet-address/', GetWalletAddress.as_view(), name='wallet-address'),
#     path('wallet-balance/', GetWalletBalance.as_view(), name='wallet-balance'),
#     path('transfer-coin/', TransferCoin.as_view(), name='transfer-coin'),
#     path('coin-swap/', CoinSwap.as_view(), name='coin-swap'),
#     path('currency-price/<str:currency>/',
#          GetCurrencyPrice.as_view(), name='currency-price'),
#     path('currency-balance/<str:currency>/',
#          GetIndividualCurrencyBalance.as_view(), name='currency-balance'),
#     path('usd-price/', GetUSDPrice.as_view(), name='usd-price'),
#     path('naira-price/', GetNairaPrice.as_view(), name='naira-price'),
#     path('usdt-to-ngn/', USDTtoNGN.as_view(), name='usdt-to-ngn'),
#     path('exchange-estimate/', GetExchangeEstimate.as_view(),
#          name='exchange-estimate'),

#     path('swap-status/<str:transaction_id>/',
#          GetSwapStatus.as_view(), name='swap-status'),

#     path('validate-currency/<str:currency>/',
#          ValidateCurrency.as_view(), name='validate-currency'),
#     path('transactions/', TransactionHistory.as_view(), name='transactions'),
#     path('transactions/<str:currency>/', CryptocurrencyTransactions.as_view(), name='cryptocurrency-transactions'),
#     path('naira-equivalent/<str:currency>/', GetNairaEquivalent.as_view(), name='getnairaequivalent')


# ]

from django.urls import path
from .views import (
    GetWalletAddress, GetWalletBalance, TransferCoin, CoinSwap, GetCurrencyPrice, TransactionHistory,
#       CryptocurrencyTransactions,
#     GetIndividualCurrencyBalance, GetUSDPrice, GetNairaPrice, USDTtoNGN, GetExchangeEstimate, GetSwapStatus, ValidateCurrency, 
    GetNairaEquivalent
)

urlpatterns = [
    path('wallet-address/', GetWalletAddress.as_view(), name='wallet-address'),
    path('wallet-balance/', GetWalletBalance.as_view(), name='wallet-balance'),
    path('transfer-coin/', TransferCoin.as_view(), name='transfer-coin'),
    path('coin-swap/', CoinSwap.as_view(), name='coin-swap'),
    path('currency-price/<str:currency>/', GetCurrencyPrice.as_view(), name='currency-price'),
#     path('currency-balance/<str:currency>/', GetIndividualCurrencyBalance.as_view(), name='currency-balance'),
#     path('usd-price/', GetUSDPrice.as_view(), name='usd-price'),
#     path('naira-price/', GetNairaPrice.as_view(), name='naira-price'),
#     path('usdt-to-ngn/', USDTtoNGN.as_view(), name='usdt-to-ngn'),
#     path('exchange-estimate/', GetExchangeEstimate.as_view(), name='exchange-estimate'),
#     path('swap-status/<str:transaction_id>/', GetSwapStatus.as_view(), name='swap-status'),
#     path('validate-currency/<str:currency>/', ValidateCurrency.as_view(), name='validate-currency'),
    path('transactions/', TransactionHistory.as_view(), name='transactions'),
#     path('transactions/<str:currency>/', CryptocurrencyTransactions.as_view(), name='cryptocurrency-transactions'),
    path('naira-equivalent/<str:currency>/', GetNairaEquivalent.as_view(), name='getnairaequivalent'),
]
