from wallet.models import Wallet
from common.responses import CustomErrorResponse
from common.utils import make_api_request
from wallet.serializers import BalanceSerializer


def get_user_balance(user):
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return 0
    
    balances = make_api_request(f'/balance/all', 'post', data={
        'btc': wallet.bitcoin_address,
        'eth': wallet.etherum_address,
        'sol': wallet.solana_address,
        'trx': wallet.tron_address,
        'usdt': wallet.usdt_address
    })
    
    serializer = BalanceSerializer(data={
        'btc_balance': balances.get('balances', {}).get('btc', "0"),
        'eth_balance': balances.get('balances', {}).get('eth', "0"),
        'sol_balance': balances.get('balances', {}).get('sol', "0"),
        'trx_balance': balances.get('balances', {}).get('trx', "0"),
        'usdt_balance': balances.get('balances', {}).get('usdt', "0")
    })
    
    if serializer.is_valid():
        return serializer.validated_data.get('total_balance', 0)
    else:
        return 0

def get_supported_currencies() -> list:
    return  ['usd', 'naira', 'btc', 'eth', 'sol', 'trx', 'usdt']

def validate_currency(currency) -> bool:
    supported_currencies= get_supported_currencies()
    
    if currency.lower() in supported_currencies:
        return True
    return False


def get_naira_equivalent(currency):
    if not validate_currency(currency):
        return None
    
    result = make_api_request(f'/price/naira')
    price = result.get(currency.upper(), None).get('price', 0)
    return price