from rest_framework import serializers
from .models import BankInformation

class BankInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInformation
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
