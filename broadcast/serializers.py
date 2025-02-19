from rest_framework import serializers
from .models import Broadcast

class BroadCastSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Broadcast
        fields = '__all__'
    
    