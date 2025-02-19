# from .serializers import *
# from common.utils import make_api_request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from .models import Wallet
# from rest_framework.generics import GenericAPIView
# from common.responses import CustomSuccessResponse, CustomErrorResponse
# from bank.models import BankInformation
# from .utils import get_naira_equivalent
# from transfer.models import Transfer
# from decimal import Decimal
# from transaction.models import Transaction
# from transaction.choices import TRANSACTION_TYPE_CHOICES
# # Create your views here.


# class GetWalletAddress(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             wallet = Wallet.objects.get(user=user)
#         except Wallet.DoesNotExist:
#             # User does not have a wallet, fetch from API
#             user_number = getattr(user, 'user_number', None)
#             if user_number is None:
#                 return CustomErrorResponse(message="User number is required", status=400)

#             result = make_api_request(f'/get_accounts/{user_number}')
#             wallet = Wallet.objects.create(
#                 user=user,
#                 bitcoin_address=result.get('btc_address', ''),
#                 solana_address=result.get('sol_address', ''),
#                 tron_address=result.get('tron_address', ''),
#                 etherum_address=result.get('eth_address', ''),
#                 usdt_address=result.get('tron_address', '')
#             )

#         serializer = WalletSerializer(wallet)
#         return CustomSuccessResponse(serializer.data, message="Wallet addresses retrieved successfully")

# # views.py (Add this to your existing views file)


# class GetWalletBalance(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             wallet = Wallet.objects.get(user=user)
#         except Wallet.DoesNotExist:
#             return CustomErrorResponse(message= "Wallet not found. Please create a wallet first.", status=404)

#         # Assuming the API returns balances for all currencies in a single request
#         balances = make_api_request(f'/balance/all', 'post', data={
#             'btc': wallet.bitcoin_address,
#             'eth': wallet.etherum_address,
#             'sol': wallet.solana_address,
#             'trx': wallet.tron_address,
#             'usdt': wallet.usdt_address
#         })

#         if len(balances['errors']):
#             return CustomErrorResponse(data= balances['errors'], status=400)

#         # Serialize the balance data
#         serializer = BalanceSerializer(data={
#             'btc_balance': balances.get('balances', {}).get('btc', "0"),
#             'eth_balance': balances.get('balances', {}).get('eth', "0"),
#             'sol_balance': balances.get('balances', {}).get('sol', "0"),
#             'trx_balance': balances.get('balances', {}).get('trx', "0"),
#             'usdt_balance': balances.get('balances', {}).get('usdt', "0")
#         })
#         # return CustomSuccessResponse(data)
#         if serializer.is_valid():
#             return CustomSuccessResponse(serializer.data, message="Wallet balances retrieved successfully")
#         else:
#             return CustomSuccessResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)


# class TransferCoin(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TransferSerializer

#     def post(self, request):
#         serializer = TransferSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             currency = data['currency']
#             amount = data['amount']
#             recipient = data['recipient']
#             path = f'/{currency}-transfer'

#             user = request.user
#             # Prepare data for the microservice API
#             api_data = {
#                 "user_number": user.user_number,
#                 # Convert decimal to string if necessary
#                 "amount": str(amount),
#                 "recipient": recipient
#             }

#             result = make_api_request(path, method='post', data=api_data)

#             if result.get('status', None) == 'Success':
#                 response_serializer = TransferResponseSerializer(data=result)
#                 if response_serializer.is_valid():
#                     #get the equivalent of the coin in naira 
#                     naira_amount = get_naira_equivalent(currency=currency) or 0

#                     #create a new transfer instance 
#                     transfer = Transfer(amount=Decimal(amount), sender=user, recipient_address=recipient, currency=currency, naira_amount=naira_amount)
#                     transfer.save()
                    
#                     #create a new transaction 
#                     transaction = Transaction(user=user, amount=amount, transaction_type=TRANSACTION_TYPE_CHOICES.TRANSFER)
#                     transaction.save()
                    
#                     return CustomSuccessResponse(response_serializer.data, message="Coin transferred successfully")
#                 return CustomErrorResponse(response_serializer.errors, status=400)
#             else:
#                 return CustomErrorResponse({"error": result.get('message')}, status=400)
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)


# # views.py (Add this to your existing views file)


# class CoinSwap(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = CoinSwapSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             from_coin = data['from_coin']
#             to_coin = data['to_coin']
#             path = f'/{from_coin}-to-{to_coin}'

#             user = request.user
#             # Prepare data for the microservice API
#             api_data = {
#                 "user_number": user.user_number,
#                 # Convert decimal to string if necessary
#                 "amount": str(data['amount'])
#             }

#             result = make_api_request(path, method='post', data=api_data)

#             if 'track' in result:
#                 response_serializer = CoinSwapResponseSerializer(data=result)
#                 if response_serializer.is_valid():
#                     return CustomSuccessResponse(response_serializer.data, message="Coin swap initiated")
#                 else:
#                     return CustomErrorResponse(response_serializer.errors, status=400)
#             else:
#                 return CustomErrorResponse(message= "Failed to initiate swap", status=400)
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)

# class GetNairaEquivalent(APIView):
#     def get(self, request, currency):
#         equivalent = get_naira_equivalent(currency)
#         return CustomSuccessResponse(data={
#             'naira_equivalent': equivalent
#         })

# class GetCurrencyPrice(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, currency):
#         if currency not in ['usd', 'naira']:
#             return CustomSuccessResponse(message="Unsupported currency", status=400)

#         result = make_api_request(f'/price/{currency}')

#         # Assuming the API returns a dictionary with cryptocurrency data keyed by symbol
#         prices = []
#         print(result)
#         for symbol, data in result.items():
#             prices.append({
#                 'name': data.get('name', ''),
#                 'symbol': symbol.upper(),
#                 'price': data.get('price', 0),
#                 'change': data.get('change', 0)
#             })

#         serializer = CurrencyPriceSerializer(data=prices, many=True)
#         if serializer.is_valid():
#             return CustomSuccessResponse(serializer.data, message="Currency prices retrieved")
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)


# class GetIndividualCurrencyBalance(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, currency):
#         user = request.user
#         try:
#             wallet = Wallet.objects.get(user=user)
#         except Wallet.DoesNotExist:
#             return CustomSuccessResponse(message="Wallet not found. Please create a wallet first.", status=404)

#         # Map currency codes to wallet attributes
#         wallet_mapping = {
#             'btc': wallet.bitcoin_address,
#             'eth': wallet.etherum_address,
#             'sol': wallet.solana_address,
#             'trx': wallet.tron_address,
#             'usdt': wallet.usdt_address
#         }

#         if currency not in wallet_mapping:
#             return CustomSuccessResponse(message= "Unsupported currency or missing wallet address", status=400)

#         address = wallet_mapping[currency]
#         if not address:
#             return CustomErrorResponse(message="No address found for specified currency", status=404)

#         result = make_api_request(
#             f'/balance/{currency}', params={'address': address})

#         serializer = IndividualCurrencyBalanceSerializer(data={
#             'currency': currency.upper(),
#             'balance': result.get(f'{currency}_balance', 0)
#         })

#         if serializer.is_valid():
#             return CustomSuccessResponse(serializer.data, message="Currency balance retrieved")
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)


# class GetUSDPrice(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = USDPriceSerializer

#     def get(self, request):
#         result = make_api_request('/price/usd')

#         # Assuming the API returns a dictionary with cryptocurrency data keyed by symbol
#         prices = []
#         for symbol, data in result.items():
#             prices.append({
#                 'name': str(data.get('name', '')),
#                 'symbol': str(symbol.upper()),
#                 'price': str(data.get('price', "0")),
#                 'change': str(data.get('change', "0"))
#             })
#         # return CustomSuccessResponse(prices)
#         serializer = USDPriceSerializer(data=prices, many=True)
#         if serializer.is_valid():
#             return CustomSuccessResponse(serializer.data, message="USD prices retrieved")
#         else:
#             return CustomSuccessResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)


# class GetNairaPrice(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         result = make_api_request('/price/naira')

#         # Assuming the API returns a dictionary with cryptocurrency data keyed by symbol
#         prices = []
#         for symbol, data in result.items():
#             prices.append({
#                 'name': data.get('name', ''),
#                 'symbol': symbol.upper(),
#                 'price': data.get('price', 0),
#                 'change': data.get('change', 0)
#             })
#         serializer = NairaPriceSerializer(data=prices, many=True)
#         if serializer.is_valid():
#             return CustomSuccessResponse(serializer.data, message= "Naira prices retrieved")
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)


# # views.py (Add this to your existing views file)


# class USDTtoNGN(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = USDTtoNGNSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             user= request.user
#             user_number = user.user_number
#             amount = data['amount']

#             try:
#                 bank = BankInformation.objects.get(user=user.id)
#             except BankInformation.DoesNotExist:
#                 return CustomErrorResponse(message="You have to fill in your bank details first")

#             # Assuming your API has a specific endpoint for USDT to NGN swap
#             result = make_api_request(f'/usdt-to-ngn', method='post', data={
#                 'user_number': user_number,
#                 'amount': str(amount),  # API might expect a string
#                 'account_number': bank.account_number,
#                 'account_bank_code': bank.bank_code,
#                 'rate':1600
#             })

#             if result.get('status') == 'Success':
#                 response_serializer = SwapResponseSerializer(data=result)
#                 if response_serializer.is_valid():
#                     return CustomSuccessResponse(response_serializer.data, message="USDT to NGN swap executed")
#                 else:
#                     return CustomErrorResponse(response_serializer.errors, status=400)
#             else:
#                 return CustomErrorResponse(message= result.get('message'), status=400)
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)


# class GetExchangeEstimate(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = ExchangeEstimateRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             from_currency = data['from_currency']
#             to_currency = data['to_currency']
#             amount = data['amount']

#             # Assuming your API has a specific endpoint for getting an exchange estimate
#             result = make_api_request(f'/exchange-estimate/{from_currency}-to-{to_currency}', method='post', data={
#                 'amount': str(amount)  # API might expect a string
#             })

#             if result.get('status') == 'Success':
#                 response_serializer = ExchangeEstimateResponseSerializer(
#                     data=result)
#                 if response_serializer.is_valid():
#                     return CustomSuccessResponse(response_serializer.data, message="Exchange estimate provided")
#                 else:
#                     return CustomErrorResponse(response_serializer.errors, status=400)
#             else:
#                 return CustomErrorResponse(message= result.get('message'), status=400)
#         else:
#             return CustomErrorResponse(serializer.errors, status=400)

# # views.py (Add this to your existing views file)


# class GetSwapStatus(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, transaction_id):
#         result = make_api_request(f'/swap-status/{transaction_id}')

#         if 'status' in result:
#             serializer = SwapStatusSerializer(data=result)
#             if serializer.is_valid():
#                 return CustomSuccessResponse(serializer.data, message="Swap status retrieved")
#             else:
#                 return CustomErrorResponse(serializer.errors, status=400)
#         else:
#             return CustomErrorResponse(message= "Failed to retrieve swap status", status=400)

# # views.py (Add this to your existing views file)


# class ValidateCurrency(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, currency):
#         supported_currencies = ['usd', 'naira',
#                                 'btc', 'eth', 'sol', 'trx', 'usdt']
#         if currency.lower() in supported_currencies:
#             return CustomSuccessResponse(message=  "Currency is supported.")
#         else:
#             return CustomErrorResponse(message="Currency is not supported.", status=404)

# class TransactionHistory(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             wallet = Wallet.objects.get(user=user)
#         except Wallet.DoesNotExist:
#             return CustomErrorResponse(message= "No wallet found for user.", status=404)

#         addresses = {
#             'btc': wallet.bitcoin_address,
#             'eth': wallet.etherum_address,
#             'tron': wallet.tron_address,
#             'solana': wallet.solana_address,
#             'usdt': wallet.usdt_address
#         }

#         # Remove any entries without an address
#         addresses = {k: v for k, v in addresses.items() if v}

#         # Make the API request
#         transactions = make_api_request('/transactions', method='post', data=addresses)

#         # Format the response uniformly
#         formatted_transactions = self.format_transactions(transactions.get('transactions', {}))

#         return CustomSuccessResponse(data= formatted_transactions)

#     def format_transactions(self, transactions):
#         formatted_data = {}
#         for currency, txns in transactions.items():
#             formatted_list = []
#             for txn in txns:
#                 formatted_txn = {
#                     "type": txn.get("type", txn.get("direction", "")),
#                     "amount": txn.get("amount"),
#                     "address": txn.get("address", txn.get("from", txn.get("to", txn.get("address_to", txn.get("address_from", "")))))
#                 }
#                 formatted_list.append(formatted_txn)
#             formatted_data[currency] = formatted_list
#         return formatted_data

# class CryptocurrencyTransactions(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, currency):
#         address = request.query_params.get('address')
#         if not address:
#             return CustomErrorResponse(message="Address parameter is required.", status=400)

#         # Make the API request to the microservice
#         response = make_api_request(f'/transactions/{currency}', params={'address': address})
        
#         # Assuming response structure is already in the described format
#         if 'error' in response:
#             return CustomErrorResponse(data= response['error'], status=400)

#         # Format the transactions uniformly
#         transactions = self.format_transactions(currency, response)
#         return CustomSuccessResponse(transactions)

#     def format_transactions(self, currency, transactions):
#         # This function adjusts the response format to make it uniform
#         key = f"{currency}_transactions"
#         if key not in transactions:
#             return {key: []}
        
#         formatted_transactions = []
#         for txn in transactions[key]:
#             formatted_txn = {
#                 "type": txn.get("type", txn.get("direction", "")),
#                 "amount": txn.get("amount"),
#                 "address": txn.get("from", txn.get("to", txn.get("address_to", txn.get("address_from", ""))))
#             }
#             formatted_transactions.append(formatted_txn)
        
#         return {key: formatted_transactions}

from .serializers import *
from common.utils import make_api_request
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from rest_framework import generics
from common.responses import CustomSuccessResponse, CustomErrorResponse
from bank.models import BankInformation
from .utils import get_naira_equivalent
from transfer.models import Transfer
from decimal import Decimal
from transaction.models import Transaction
from transaction.choices import TRANSACTION_TYPE_CHOICES


class GetWalletAddress(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer

    def get(self, request):
        user = request.user
        wallet = self.get_user_wallet(user)
        if isinstance(wallet, CustomErrorResponse):
            return wallet
        
        serializer = self.serializer_class(wallet)
        return CustomSuccessResponse(serializer.data, message="Wallet addresses retrieved successfully")

    def get_user_wallet(self, user):
        try:
            return Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            return self.create_wallet_for_user(user)

    def create_wallet_for_user(self, user):
        user_number = getattr(user, 'user_number', None)
        if not user_number:
            return CustomErrorResponse(message="User number is required", status=400)

        result = make_api_request(f'/get_accounts/{user_number}')
        return Wallet.objects.create(
            user=user,
            bitcoin_address=result.get('btc_address', ''),
            solana_address=result.get('sol_address', ''),
            tron_address=result.get('tron_address', ''),
            etherum_address=result.get('eth_address', ''),
            usdt_address=result.get('tron_address', '')
        )


class GetWalletBalance(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BalanceSerializer

    def get(self, request):
        user = request.user
        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            return CustomErrorResponse(message="Wallet not found. Please create a wallet first.", status=404)

        balance_data = self.get_balances(wallet)
        serializer = self.serializer_class(data=balance_data)

        if serializer.is_valid():
            return CustomSuccessResponse(serializer.data, message="Wallet balances retrieved successfully")
        return CustomErrorResponse(serializer.errors, status=400)

    def get_balances(self, wallet):
        balances = make_api_request('/balance/all', 'post', data={
            'btc': wallet.bitcoin_address,
            'eth': wallet.etherum_address,
            'sol': wallet.solana_address,
            'trx': wallet.tron_address,
            'usdt': wallet.usdt_address
        })

        return {
            'btc_balance': balances.get('balances', {}).get('btc', "0"),
            'eth_balance': balances.get('balances', {}).get('eth', "0"),
            'sol_balance': balances.get('balances', {}).get('sol', "0"),
            'trx_balance': balances.get('balances', {}).get('trx', "0"),
            'usdt_balance': balances.get('balances', {}).get('usdt', "0")
        }


class TransferCoin(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = self.perform_transfer(request.user, data)
            return response
        return CustomErrorResponse(serializer.errors, status=400)

    def perform_transfer(self, user, data):
        api_data = {
            "user_number": user.user_number,
            "amount": str(data['amount']),
            "recipient": data['recipient']
        }

        path = f'/{data["currency"]}-transfer'
        result = make_api_request(path, method='post', data=api_data)

        if result.get('status') == 'Success':
            return self.save_transfer_and_transaction(user, data, result)
        return CustomErrorResponse({"error": result.get('message')}, status=400)

    def save_transfer_and_transaction(self, user, data, result):
        naira_amount = get_naira_equivalent(currency=data['currency']) or 0

        Transfer.objects.create(
            amount=Decimal(data['amount']),
            sender=user,
            recipient_address=data['recipient'],
            currency=data['currency'],
            naira_amount=naira_amount
        )

        Transaction.objects.create(
            user=user,
            amount=data['amount'],
            transaction_type=TRANSACTION_TYPE_CHOICES.TRANSFER
        )

        response_serializer = TransferResponseSerializer(data=result)
        if response_serializer.is_valid():
            return CustomSuccessResponse(response_serializer.data, message="Coin transferred successfully")
        return CustomErrorResponse(response_serializer.errors, status=400)


class CoinSwap(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoinSwapSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return self.perform_coin_swap(request.user, serializer.validated_data)
        return CustomErrorResponse(serializer.errors, status=400)

    def perform_coin_swap(self, user, data):
        path = f'/{data["from_coin"]}-to-{data["to_coin"]}'
        result = make_api_request(path, method='post', data={
            "user_number": user.user_number,
            "amount": str(data['amount'])
        })

        if 'track' in result:
            response_serializer = CoinSwapResponseSerializer(data=result)
            if response_serializer.is_valid():
                return CustomSuccessResponse(response_serializer.data, message="Coin swap initiated")
            return CustomErrorResponse(response_serializer.errors, status=400)
        return CustomErrorResponse(message="Failed to initiate swap", status=400)


class GetNairaEquivalent(generics.GenericAPIView):
    def get(self, request, currency):
        equivalent = get_naira_equivalent(currency)
        return CustomSuccessResponse(data={'naira_equivalent': equivalent})


class GetCurrencyPrice(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencyPriceSerializer

    def get(self, request, currency):
        if currency not in ['usd', 'naira']:
            return CustomErrorResponse(message="Unsupported currency", status=400)

        result = make_api_request(f'/price/{currency}')
        prices = [
            {
                'name': data.get('name', ''),
                'symbol': symbol.upper(),
                'price': data.get('price', 0),
                'change': data.get('change', 0)
            }
            for symbol, data in result.items()
        ]

        serializer = self.serializer_class(data=prices, many=True)
        if serializer.is_valid():
            return CustomSuccessResponse(serializer.data, message="Currency prices retrieved")
        return CustomErrorResponse(serializer.errors, status=400)


class TransactionHistory(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wallet = self.get_user_wallet(user)
        if isinstance(wallet, CustomErrorResponse):
            return wallet

        addresses = self.get_user_addresses(wallet)
        transactions = make_api_request('/transactions', method='post', data=addresses)
        formatted_transactions = self.format_transactions(transactions.get('transactions', {}))

        return CustomSuccessResponse(data=formatted_transactions)

    def get_user_wallet(self, user):
        try:
            return Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            return CustomErrorResponse(message="No wallet found for user.", status=404)

    def get_user_addresses(self, wallet):
        return {k: v for k, v in {
            'btc': wallet.bitcoin_address,
            'eth': wallet.etherum_address,
            'trx': wallet.tron_address,
            'sol': wallet.solana_address,
            'usdt': wallet.usdt_address
        }.items() if v}

    def format_transactions(self, transactions):
        formatted_data = {}
        for currency, txns in transactions.items():
            formatted_data[currency] = [
                {
                    "type": txn.get("type", txn.get("direction", "")),
                    "amount": txn.get("amount"),
                    "address": txn.get("address", txn.get("from", txn.get("to", "")))
                }
                for txn in txns
            ]
        return formatted_data
