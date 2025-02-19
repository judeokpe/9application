from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from common.responses import CustomSuccessResponse
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = UserProfileSerializer  

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class()

    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(instance=user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomSuccessResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return CustomSuccessResponse(data=serializer.data)