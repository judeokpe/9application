from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser
from common.responses import CustomErrorResponse, CustomSuccessResponse
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import ChatMessage, Thread
from .serializers import ChatMessageSerializer, ThreadSerializer, UplaodChatWithAttachmentSerializer
import uuid
from rest_framework import generics

class GetChatMessageApi(APIView):
    """
    Gets all the chat messages between the currently authenticated user and the user with the provided uid
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        user = request.user
        
        try: 
            user_two = CustomUser.objects.get(id=uid)
        except (CustomUser.DoesNotExist, ValidationError):
            return CustomErrorResponse(status=404, message='Invalid receipient')
        
        lookup_one = Q(sender=user, receiver=user_two)
        lookup_two = Q(sender=user_two, receiver=user)

        chat_messages = ChatMessage.objects.filter(lookup_one | lookup_two).order_by('created')
        chat_serializer = ChatMessageSerializer(chat_messages, many=True)

        return CustomSuccessResponse(data={
            "messages": chat_serializer.data
        }, message="Messages retreived successfully")
        


class GetUserThreads(APIView):
    """
    Gets all the threads the currently logged in user is involved in
        
    ---
    A thread represents a conversation between two users
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        threads= ThreadSerializer(Thread.threadm.by_user(user), many=True)
        return CustomSuccessResponse(data=threads.data)

    
