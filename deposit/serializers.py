from rest_framework import serializers
from .models import Deposit
from account.serializer import UserMainSerializer

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'deposit'
        model = Deposit
        exclude = ['naira_amount']
        read_only_fields = ['user', 'created', 'verified', 'naira_amount']
        
        
class DepositListSerializer(serializers.ModelSerializer):
    user = UserMainSerializer()
    class Meta:
        ref_name = 'deposit_list'
        model = Deposit
        fields = '__all__'
        

class DepositVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['verified']
