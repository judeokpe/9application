from rest_framework import serializers
from .models import Withdrawal

class WithdrawalSerializer(serializers.ModelSerializer):
    wallet_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Withdrawal
        fields = ['id', 'created', 'amount', 'wallet_type', 'wallet_address', 'naira_amount', 'verified', 'wallet_type_display']
        read_only_fields = ['id', 'created', 'verified']

    def get_wallet_type_display(self, obj):
        return obj.get_wallet_type_display()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['wallet_type_display'] == "":
            representation['wallet_type_display'] = "Local Bank"
        return representation



class WithdrawalVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['verified']


class LocalBankWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['amount', 'naira_amount', 'bank_name', 'account_number', 'account_name']
        extra_kwargs = {
            'bank_name': {'max_length': 100, 'required': True},
            'account_number': {'max_length': 50, 'required': True},
            'account_name': {'max_length': 255,'required': True}
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        # Create and return the Withdrawal instance with the validated data
        return Withdrawal.objects.create(**validated_data)
