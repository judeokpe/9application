from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import PermissionDenied
from .models import BankInformation
from .serializers import BankInformationSerializer

class BankInformationListCreateView(generics.ListCreateAPIView):
    queryset = BankInformation.objects.all()
    serializer_class = BankInformationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict the queryset to only the authenticated user's bank information
        return BankInformation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        # Check if the user already has a bank information entry
        if BankInformation.objects.filter(user=user).exists():
            raise serializers.ValidationError("Bank information already exists for this user.")
        serializer.save(user=user)

class BankInformationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankInformation.objects.all()
    serializer_class = BankInformationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        # Ensure the user is only accessing their own bank information
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this bank information.")
        return obj
