# from rest_framework import serializers
# from .models import Wallet


# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ['bitcoin_address', 'solana_address',
#                   'tron_address', 'etherum_address', 'usdt_address']

# # serializers.py (Add this to your existing serializers file)


# class BalanceSerializer(serializers.Serializer):
#     btc_balance = serializers.FloatField()
#     eth_balance = serializers.FloatField()
#     sol_balance = serializers.FloatField()
#     trx_balance = serializers.FloatField()
#     usdt_balance = serializers.FloatField()
    
#     total_balance = serializers.SerializerMethodField()
    
#     def get_total_balance(self, obj):
#         total = sum([obj.btc_balance, obj.eth_balance,
#                     obj.sol_balance, obj.trx_balance, obj.usdt_balance])
#         return total

# # serializers.py (Add this to your existing serializers file)


# class TransferSerializer(serializers.Serializer):
#     amount = serializers.CharField(max_length=255)
#     recipient = serializers.CharField(max_length=200)
#     # You might define choices if you want stricter control
#     currency = serializers.CharField(max_length=5)


# class TransferResponseSerializer(serializers.Serializer):
#     transaction_id = serializers.CharField(max_length=200)
#     status = serializers.CharField(max_length=20)
#     message = serializers.CharField(max_length=200)

# # serializers.py (Add this to your existing serializers file)


# class CoinSwapSerializer(serializers.Serializer):
#     amount = serializers.CharField(max_length=255)
#     from_coin = serializers.CharField(max_length=5)
#     to_coin = serializers.CharField(max_length=5)


# class CoinSwapResponseSerializer(serializers.Serializer):
#     track = serializers.CharField(max_length=200)
#     response_text = serializers.CharField(max_length=200)

# # serializers.py (Add this to your existing serializers file)


# class CurrencyPriceSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50)
#     symbol = serializers.CharField(max_length=10)
#     price = serializers.CharField(max_length=255)
#     change = serializers.CharField(max_length=255)

# # serializers.py (Add this to your existing serializers file)


# class IndividualCurrencyBalanceSerializer(serializers.Serializer):
#     currency = serializers.CharField(max_length=5)
#     balance = serializers.CharField(max_length=255)

# # serializers.py (Add this to your existing serializers file)


# class USDPriceSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50)
#     symbol = serializers.CharField(max_length=10)
#     price = serializers.CharField(max_length=255)
#     change = serializers.CharField(max_length=255)

# # serializers.py (Add this to your existing serializers file)


# class NairaPriceSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50)
#     symbol = serializers.CharField(max_length=10)
#     price = serializers.CharField(max_length=255)
#     change = serializers.CharField(max_length=255)

# # serializers.py (Add this to your existing serializers file)


# class USDTtoNGNSerializer(serializers.Serializer):
#     amount = serializers.CharField(max_length=255)


# class SwapResponseSerializer(serializers.Serializer):
#     transaction_id = serializers.CharField(max_length=200)
#     swapped_amount = serializers.CharField(max_length=255)
#     status = serializers.CharField(max_length=50)
#     message = serializers.CharField(max_length=200)

# # serializers.py (Add this to your existing serializers file)


# class ExchangeEstimateRequestSerializer(serializers.Serializer):
#     from_currency = serializers.CharField(max_length=5)
#     to_currency = serializers.CharField(max_length=5)
#     amount = serializers.CharField(max_length=255)


# class ExchangeEstimateResponseSerializer(serializers.Serializer):
#     estimated_amount = serializers.CharField(max_length=255)
#     rate = serializers.DecimalField(max_digits=16, decimal_places=8)
#     status = serializers.CharField(max_length=50)
#     message = serializers.CharField(max_length=200)


# # serializers.py (Add this to your existing serializers file)

# class SwapStatusSerializer(serializers.Serializer):
#     transaction_id = serializers.CharField(max_length=200)
#     status = serializers.CharField(max_length=50)
#     message = serializers.CharField(max_length=200)


from rest_framework import serializers
from .models import Wallet


# Wallet Addresses Serializer
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'bitcoin_address',
            'solana_address',
            'tron_address',
            'ethereum_address',
            'usdt_address'
        ]


# Wallet Balance Serializer
class BalanceSerializer(serializers.Serializer):
    btc_balance = serializers.DecimalField(max_digits=20, decimal_places=8)
    eth_balance = serializers.DecimalField(max_digits=20, decimal_places=8)
    sol_balance = serializers.DecimalField(max_digits=20, decimal_places=8)
    trx_balance = serializers.DecimalField(max_digits=20, decimal_places=8)
    usdt_balance = serializers.DecimalField(max_digits=20, decimal_places=8)

    total_balance = serializers.SerializerMethodField()

    def get_total_balance(self, obj):
        total = sum([
            obj['btc_balance'], obj['eth_balance'],
            obj['sol_balance'], obj['trx_balance'],
            obj['usdt_balance']
        ])
        return total


# Transfer Request Serializer
class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    recipient = serializers.CharField(max_length=200)
    currency = serializers.ChoiceField(choices=['BTC', 'ETH', 'SOL', 'TRX', 'USDT'])


# Transfer Response Serializer
class TransferResponseSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=200)


# Coin Swap Request Serializer
class CoinSwapSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    from_coin = serializers.ChoiceField(choices=['BTC', 'ETH', 'SOL', 'TRX', 'USDT'])
    to_coin = serializers.ChoiceField(choices=['BTC', 'ETH', 'SOL', 'TRX', 'USDT'])


# Coin Swap Response Serializer
class CoinSwapResponseSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=200)
    swapped_amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    status = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=200)


# Currency Price Serializer
class CurrencyPriceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    symbol = serializers.CharField(max_length=10)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    change = serializers.DecimalField(max_digits=6, decimal_places=2)


# Individual Currency Balance Serializer
class IndividualCurrencyBalanceSerializer(serializers.Serializer):
    currency = serializers.CharField(max_length=5)
    balance = serializers.DecimalField(max_digits=20, decimal_places=8)


# USD Price Serializer
class USDPriceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    symbol = serializers.CharField(max_length=10)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    change = serializers.DecimalField(max_digits=6, decimal_places=2)


# Naira Price Serializer
class NairaPriceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    symbol = serializers.CharField(max_length=10)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    change = serializers.DecimalField(max_digits=6, decimal_places=2)


# USDT to NGN Conversion Serializer
class USDTtoNGNSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)


# Swap Response Serializer
class SwapResponseSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=200)
    swapped_amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    status = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=200)


# Exchange Estimate Request Serializer
class ExchangeEstimateRequestSerializer(serializers.Serializer):
    from_currency = serializers.ChoiceField(choices=['BTC', 'ETH', 'SOL', 'TRX', 'USDT'])
    to_currency = serializers.ChoiceField(choices=['BTC', 'ETH', 'SOL', 'TRX', 'USDT'])
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)


# Exchange Estimate Response Serializer
class ExchangeEstimateResponseSerializer(serializers.Serializer):
    estimated_amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    rate = serializers.DecimalField(max_digits=16, decimal_places=8)
    status = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=200)


# Swap Status Serializer
class SwapStatusSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=200)
