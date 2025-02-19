from transaction.choices import TRANSACTION_TYPE_CHOICES
from transaction.models import Transaction
from django.db.models import Sum
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from transfer.models import Transfer




def get_user_total_deposit(user):
    total = get_total_deposit(Deposit.objects.filter(user=user))
    return total


def get_user_total_transfer(user):
    return get_total_transfer(Transfer.objects.filter(sender=user))


def get_user_total_withdrawal(user):
    return get_total_withdrawal(Withdrawal.objects.filter(user=user))


def get_total_transfer(base_query=Transfer.objects.all()):
    total_transfer = base_query.aggregate(total=Sum('naira_amount'))['total'] or 0
    return total_transfer

def get_total_deposit(base_query=Deposit.objects.all()):
    total_deposit = base_query.aggregate(total=Sum('naira_amount'))['total'] or 0
    return total_deposit


def get_total_withdrawal(base_query=Withdrawal.objects.all()):
    total_deposit = base_query.aggregate(total=Sum('naira_amount'))['total'] or 0
    return total_deposit