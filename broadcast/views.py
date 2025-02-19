from django.shortcuts import render
from rest_framework import generics
from .tasks import email_broadcast, sms_broadcast, EmailBroadcastThread, SMSBroadcastThread
from common.responses import CustomSuccessResponse, CustomErrorResponse
from .serializers import BroadCastSerializer
from common.utils import get_first_error

# Create your views here.


class EmailBroadCastApi(generics.GenericAPIView):
    serializer_class = BroadCastSerializer
    def get(self, request):
        return CustomSuccessResponse(message='Test mode')
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            
            message = serializer.validated_data.get('message')
            subject = serializer.validated_data.get('subject')
            serializer.save()
            # email_broadcast.delay(message, subject)
            # email_broadcast(message, subject)
            EmailBroadcastThread(message=message, subject=subject).start()
            return CustomSuccessResponse(message="Emails distributed successfully")
        else:
            return CustomErrorResponse(message=get_first_error(serializer.errors), data={})
        
    
class SmsBroadcastApi(generics.GenericAPIView):
    serializer_class = BroadCastSerializer
    def get(self, request):
        return CustomSuccessResponse(message='Test mode')
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get('message')
            
            SMSBroadcastThread(message=message).start()
        return CustomSuccessResponse(message="SMS broadcast successfull")

