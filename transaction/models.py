from django.db import models
from account.models import CustomUser
from common.models import BaseModel
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from .choices import TRANSACTION_TYPE_CHOICES

class Transaction(BaseModel):
    # TRANSACTION_TYPE_CHOICES = (
    #     ('DEPOSIT', 'Deposit'),
    #     ('WITHDRAWAL', 'Withdrawal'),
    # )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES.choices, max_length=10)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.get_transaction_type_display()} of {self.amount}'

    def get_status(self):
        if self.transaction_type == 'DEPOSIT':
            if self.deposit and self.deposit.verified:
                return 'APPROVED'
            else:
                return 'PENDING'
        elif self.transaction_type == 'WITHDRAWAL':
            if self.withdrawal and self.withdrawal.verified:
                return 'APPROVED'
            else:
                return 'PENDING'
        elif self.transaction_type == 'TRANSFER':
            return 'APPROVED'#as far as a transfer is successful, it is approved
        else:
            return 'UNKNOWN'


    def set_status(self, value):
        # Do something with the value if needed
        pass

    status = property(get_status, set_status)
