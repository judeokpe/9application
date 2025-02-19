from rest_framework import serializers
from .models import CustomUser, Pin
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'available_balance')

        extra_kwargs = {
            'password': {'write_only': True},
            'available_balance': {'read_only': True}
        }
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
        )
        return user


class VerifyAccountSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField(required=True)
    # phone_number = serializers.CharField(required=False)

class VerifyAccountSmsSerializer(serializers.Serializer):
    otp = serializers.CharField()
    phone_number = serializers.CharField(required=False)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TwoFactorAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['two_factor_enabled', "two_factor_type"]


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordRestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        if len(password) < 8:
            raise serializers.ValidationError({'Password': 'Password is not strong!'})
        return attrs


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()




class PhoneSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    def validate_phone_number(self, value):
        # Additional validation if needed
        if not value.is_valid():
            raise serializers.ValidationError("Invalid phone number format.")
        return value


class PasswordResetConfirmationSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    otp = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        otp = attrs.get('otp')
        email = attrs.get('email')

        if len(new_password) < 8:
            raise serializers.ValidationError({'new_password': 'Password must be at least 8 characters long'})

        return attrs



class PasswordResetConfirmationPhoneSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    otp = serializers.CharField(write_only=True, max_length=6)

    def validate_new_password(self, value):
        # Add password validation logic if necessary
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

class VerificationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ['id', 'user', 'pin']

class CreatPinSerializer(serializers.Serializer):
    pin = serializers.CharField()

class ComparePinSerializer(serializers.Serializer):
    pin = serializers.CharField()

class ChangePinSerializer(serializers.Serializer):
    old_pin = serializers.CharField()
    new_pin = serializers.CharField()

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['has_kyc']

class UserMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email','first_name', 'last_name','phone_number', 'has_kyc', 'two_factor_enabled','two_factor_type','has_kyc']


class ExecUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'has_kyc', 'two_factor_enabled', 'two_factor_type', 'has_kyc']



# class TwoFactorAuthSerializerRequest(serializers.Serializer):
#     two_factor_type = serializers.ChoiceField(choices=["email", "phone_number"])
    
#     def validate(self, data):
#         user = self.context["request"].user
#         # if not user.has_kyc:
#         #     raise serializers.ValidationError("KYC verification is required for 2FA.")
#         if data["two_factor_type"] == "phone_number" and not user.phone_number:
#             raise serializers.ValidationError("Phone number is required for SMS-based 2FA.")
#         return data

class TwoFactorAuthSerializerRequest(serializers.Serializer):
    two_factor_type = serializers.ChoiceField(choices=["email", "phone_number"])

    def validate(self, data):
        user = self.context["request"].user
        if data["two_factor_type"] == "email" and not user.email:
            raise serializers.ValidationError("Email is required for email-based 2FA.")
        if data["two_factor_type"] == "phone_number" and not user.phone_number:
            raise serializers.ValidationError("Phone number is required for SMS-based 2FA.")
        return data



class VerifyOTPSerializer2fa(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    