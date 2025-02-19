from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from common.responses import *
from rest_framework.generics import GenericAPIView, CreateAPIView
from .serializer import *
from .models import CustomUser,Pin
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.db import transaction
from .utils import send_activation_email
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from common.utils import send_2fa_enable_mail, send_reset_request_sms, send_verify_mail, get_and_save_otp, send_sms, send_reset_request_mail, hashword, compare_word
from django.db import IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.generics import GenericAPIView

from .models import CustomUser
# from .utils import CustomErrorResponse, CustomErrorResponse404, CustomSuccessResponse, send_sms, get_and_save_otp
from django.core.cache import cache

# Create your views here.


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        
        #    # Disable registration by returning a custom error response
        # return CustomErrorResponse(
        #     message="Registration is currently disabled.",
        #     status=status.HTTP_403_FORBIDDEN
        # )
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            # Extract validated data
            validated_data = serializer.validated_data
            # Set password
            password = validated_data['password']
            validated_data['password'] = make_password(password)

            try:
                user = serializer.save()
            except IntegrityError as e:
                if 'UNIQUE constraint failed: account_customuser.email' in str(e):
                    return CustomErrorResponse(message='A user with that email already exists.', status=status.HTTP_400_BAD_REQUEST)
                elif 'UNIQUE constraint failed: account_customuser.phone_number' in str(e):
                    return CustomErrorResponse(message= 'A user with that phone number already exists.', status=status.HTTP_400_BAD_REQUEST)
                else:
                    return CustomErrorResponse(message= str(e), status=status.HTTP_400_BAD_REQUEST)

            otp = get_and_save_otp(user.email)
            # Generate OTP and send activation email
            send_verify_mail(user, otp)
            # Return custom success response
            return CustomSuccessResponse(
                message="OTP for account activation sent successfully",
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            print(errors)
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)



class ResendOTPView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResendOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
        
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone_number')

            if (not email and not phone):
                CustomErrorResponse(
                    message="phone_number or email must be provided", status=status.HTTP_400_BAD_REQUEST)

            try:
                if email:
                    # Check if the email exists in the database
                    try:
                        user = CustomUser.objects.get(email=email)
                    except CustomUser.DoesNotExist:
                        return CustomErrorResponse404(message="Email not found")

                    otp = get_and_save_otp(user.email)
                    # Generate OTP and send activation email
                    send_verify_mail(user, otp)
                    return CustomSuccessResponse(message="OTP resent successfully")

                if phone:
                    # Check if the phone exists in the database
                    try:
                        user = CustomUser.objects.get(phone_number=phone)
                    except CustomUser.DoesNotExist:
                        return CustomErrorResponse404(message="Phone number not found")

                    otp = get_and_save_otp(user.phone_number)
                    # Generate OTP and send activation sms
                    send_sms(user.phone_number, f"Your OTP is: {otp}. It will expire in 5 minutes.")
                    return CustomSuccessResponse(message="OTP resent successfully")


            except Exception as err:
                return CustomErrorResponse(data=str(err), status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            print(errors)
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)





class VerifyAccountAPI(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            otp = serializer.validated_data.get('otp')
            email = serializer.validated_data.get('email')

            if not email:
                return CustomErrorResponse(
                    message="Email must be provided", status=status.HTTP_400_BAD_REQUEST
                )

            # Retrieve OTP from cache
            cached_otp = cache.get(email)
            if cached_otp is None:
                return CustomErrorResponse(
                    message="OTP has expired or is invalid", status=status.HTTP_400_BAD_REQUEST
                )

            # Check if OTP is correct
            if otp == cached_otp:
                try:
                    user = CustomUser.objects.get(email=email)
                except CustomUser.DoesNotExist:
                    return CustomErrorResponse404(message="Email not found")
                
                user.email_verified = True
                user.save()
                cache.delete(email)

                # Generate OTP and send SMS for phone verification
                otp = get_and_save_otp(user.phone_number)
                send_sms(user.phone_number, f"Your OTP is: {otp}. It will expire in 5 minutes.")

                return CustomSuccessResponse(message="Email verified successfully and SMS sent")
            else:
                return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)
        
        except serializers.ValidationError as e:
            # Clean up error message formatting
            message = ' '.join([error[0].replace('custom', '').strip().capitalize() for error in e.detail.values()])
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            return CustomErrorResponse(data=str(err), status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneNumber(generics.GenericAPIView):
    serializer_class = VerifyAccountSmsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            otp = serializer.validated_data.get('otp')
            phone_number = serializer.validated_data.get('phone_number')

            if not phone_number:
                return CustomErrorResponse(
                    message="Phone number must be provided", status=status.HTTP_400_BAD_REQUEST
                )

            # Retrieve OTP from cache
            cached_otp = cache.get(phone_number)
            if otp == cached_otp:
                try:
                    user = CustomUser.objects.get(phone_number=phone_number)
                except CustomUser.DoesNotExist:
                    return CustomErrorResponse404(message="Phone number not found")

                user.phone_number_verified = True
                if user.email_verified:
                    user.is_active = True
                user.save()
                cache.delete(phone_number)

                return CustomSuccessResponse(message="Account verified successfully")
            else:
                return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as e:
            # Standardize error message formatting
            message = ' '.join([error[0].replace('custom', '').strip().capitalize() for error in e.detail.values()])
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            return CustomErrorResponse(data=str(err), status=status.HTTP_400_BAD_REQUEST)

# Login API


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.none()  # Return empty queryset

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                raise serializers.ValidationError(
                    {"email":["Email and password are required"]})

            # Check if user exists
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("User does not exist")

            # Check if user is active
            if not user.is_active:
                send_activation_email(user)
                raise serializers.ValidationError(
                    {"user": ["This user is currently not active. Verify your account"]})

            # Authenticate user
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError({"user":["Invalid login details"]})

            if user.two_factor_enabled:
                # Generate and cache OTP
                if user.two_factor_type == "email":
                    otp = get_and_save_otp(user.email)
                    send_verify_mail(user, otp)
                else:
                    otp = get_and_save_otp(user.phone_number)
                    send_sms(user.phone_number, otp)
                # Send OTP to user via email or SMS (not implemented here)
                return CustomSuccessResponse(message="OTP sent successfully")

            # Generate tokens if 2FA is not enabled
            refresh = RefreshToken.for_user(user)
            return CustomSuccessResponse(data={
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })

        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                try:
                    message += errors[i][0]
                except TypeError:
                    message += i
                except:
                    message += "login not successful"    
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)
        
class AdminLoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.none()  # Return empty queryset

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                raise serializers.ValidationError(
                    {"email":["Email and password are required"]})

            # Check if user exists
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("User does not exist")

            if not user.is_staff:
                return CustomErrorResponse(message="Account associated with that email is not an admin account")
            # Check if user is active
            if not user.is_active:
                send_activation_email(user)
                raise serializers.ValidationError(
                    {"user": ["This user is currently not active. Verify your account"]})

            # Authenticate user
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError({"user":["Invalid login details"]})

            if user.two_factor_enabled:
                # Generate and cache OTP
                if user.two_factor_type == "email":
                    otp = get_and_save_otp(user.email)
                    send_verify_mail(user, otp)
                else:
                    otp = get_and_save_otp(user.phone_number)
                    send_sms(user.phone_number, otp)
                # Send OTP to user via email or SMS (not implemented here)
                return CustomSuccessResponse(message="OTP sent successfully")

            # Generate tokens if 2FA is not enabled
            refresh = RefreshToken.for_user(user)
            return CustomSuccessResponse(data={
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })

        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                try:
                    message += errors[i][0]
                except TypeError:
                    message += i
                except:
                    message += "login not successful"    
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)



class TwoFactorAuthVerificationAPI(APIView):
    serializer_class = VerifyAccountSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            otp = serializer.validated_data.get('otp')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')

            if (not email and not phone_number):
                CustomErrorResponse(
                    message="phone_number or email must be provided", status=status.HTTP_400_BAD_REQUEST)

            # Retrieve OTP from cache
            try:
                if email:
                    cached_otp = cache.get(email)
                    # Check if the email exists in the database
                    if otp == cached_otp:
                        try:
                            user = CustomUser.objects.get(email=email)
                        except CustomUser.DoesNotExist:
                            return CustomErrorResponse404(message="Email not found")
                        cache.delete(email)
                        refresh = RefreshToken.for_user(user)
                    #  Access serializer context from the request
                        serializer_context = {'request': request}

                        return CustomSuccessResponse(data={
                            'user': UserSerializer(user, context=serializer_context).data,
                            'token': str(refresh.access_token),
                            'refresh_token': str(refresh)
                        })
                    else:
                        return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)

                if phone_number:
                    cached_otp = cache.get(phone_number)
                    # Check if the email exists in the database
                    print(cached_otp)
                    if otp == cached_otp:
                        try:
                            user = CustomUser.objects.get(
                                phone_number=phone_number)
                        except CustomUser.DoesNotExist:
                            return CustomErrorResponse404(message="Phone number not found")
                        cache.delete(phone_number)

                        refresh = RefreshToken.for_user(user)
                    #  Access serializer context from the request
                        serializer_context = {'request': request}

                        return CustomSuccessResponse(data={
                            'user': UserSerializer(user, context=serializer_context).data,
                            'token': str(refresh.access_token),
                            'refresh_token': str(refresh)
                        })
                    else:
                        return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)

            except Exception as err:
                return CustomErrorResponse(data=str(err), status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)



class TwoFactorAuthAPI(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = TwoFactorAuthSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=request.user, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomSuccessResponse(data=serializer.data)
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)

# View User Api


class UserListViewAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# Logout Api

class LogoutAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:    
            serializer.is_valid(raise_exception=True)

            try:
                refresh_token = serializer.validated_data['refresh_token']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return CustomSuccessResponse(message="User logged out successfully.")
            except Exception as e:
                return CustomErrorResponse(message="Invalid refresh token.", status=status.HTTP_400_BAD_REQUEST)
            
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)


# Change Password API


class ChangePassword(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            # Check if the old password matches the user's current password
            if not user.check_password(serializer.validated_data['old_password']):
                return CustomErrorResponse(message="Old password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                # Change the password
                user.set_password(serializer.validated_data['new_password'])
                user.save()

                # Invalidate existing tokens
                refresh_token = RefreshToken.for_user(user)
                return CustomSuccessResponse(data={
                    'refresh_token': str(refresh_token)
                }, message='Password changed successfully.')

        else:
            errors = serializer.errors
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message==message, status=status.HTTP_400_BAD_REQUEST)

# Password Reset API


class PasswordResetView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            email = validated_data.get('email')

            # Check if the email exists in the database
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return CustomErrorResponse404(message="Email not found")


            otp = get_and_save_otp(user.email)
        # Generate OTP and send activation email
            send_reset_request_mail(user, otp)
        
            return CustomSuccessResponse(message="password reset OTP sent successfully")
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return CustomErrorResponse(data=str(err), status=status.HTTP_400_BAD_REQUEST)


class PasswordResetPhoneView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneSerializer  # Use serializer for validating phone numbers

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            phone_number = validated_data.get('phone_number')

            # Check if the phone number exists in the database
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return CustomErrorResponse404(message="Phone number not found")

            # Generate OTP and save it
            otp = get_and_save_otp(user.phone_number)
            
            # Send OTP to user's phone number via SMS
            send_reset_request_sms(user, otp)

            return CustomSuccessResponse(message="Password reset OTP sent successfully via SMS")
        
        except serializers.ValidationError as e:
            errors = e.detail
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            return CustomErrorResponse(data=str(err), status=status.HTTP_400_BAD_REQUEST)


# reset the user password with the new password, the token is the one that was sent from VerifyTokenView
class PasswordResetConfirmationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmationSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Get new password and OTP from validated data
                new_password = validated_data.get('new_password')
                otp = validated_data.get('otp')
                email = validated_data.get('email')

                # Retrieve OTP from cache
                cached_otp = cache.get(email)

                # Check if the provided OTP matches the one stored in the cache
                if otp != cached_otp:
                    return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)
                try:
                # Find user by email
                    user = CustomUser.objects.get(email=email)
                except CustomUser.DoesNotExist:
                    return CustomErrorResponse404(message="User not found")
                # Set new password
                user.set_password(new_password)
                user.save()

                # Clear OTP from cache after successful password reset
                cache.delete(email)

                return CustomSuccessResponse(message="Password reset successfully")
            errors = serializer.errors
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message =message, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmationPhoneView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmationPhoneSerializer  # Phone-based serializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Get new password, OTP, and phone number from validated data
            new_password = validated_data.get('new_password')
            otp = validated_data.get('otp')
            phone_number = validated_data.get('phone_number')

            # Retrieve OTP from cache using phone number
            cached_otp = cache.get(phone_number)

            # Check if the provided OTP matches the one stored in the cache
            if otp != cached_otp:
                return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Find user by phone number
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return CustomErrorResponse404(message="User not found")

            # Set new password
            user.set_password(new_password)
            user.save()

            # Clear OTP from cache after successful password reset
            cache.delete(phone_number)

            return CustomSuccessResponse(message="Password reset successfully")
        
        # Handle serializer validation errors
        errors = serializer.errors
        message = ""
        for i in errors:
            message += errors[i][0]
        message = message.replace('custom', '').strip().capitalize()
        return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)

# verify the token for forget password that the user got from his email and sends a frontend a token which they will use when the user is sumbinting the new password 
class VerifyTokenView(generics.CreateAPIView):
    serializer_class = VerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = serializer.validated_data.get("otp")

            cached_otp = cache.get(email)
            if otp != cached_otp:
                return CustomErrorResponse(message="Invalid OTP", status=status.HTTP_400_BAD_REQUEST)
            else:
                verification_code = get_and_save_otp(email, 5, 3600)          
            return CustomSuccessResponse({"new_verification_code": verification_code}, status=status.HTTP_200_OK)
        errors = serializer.errors
        message = ""
        for i in errors:
            message += errors[i][0]
        message = message.replace('custom', '').strip().capitalize()
        return CustomErrorResponse(message =message, status=status.HTTP_400_BAD_REQUEST)

class CreatPinView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatPinSerializer
    
    def post(self, request):
        serializer = CreatPinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        pin = serializer.validated_data.get('pin')
        
        if Pin.objects.filter(user=user).exists():
            return CustomErrorResponse(message="User pin already exists", status=400)
        
        hashed_pin = hashword(str(pin))
        Pin.objects.create(user=user, pin=hashed_pin)
        return CustomSuccessResponse(message="Pin has been set", status=200)

class ComparePin(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComparePinSerializer

    def post(self, request):
        serializer = ComparePinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        pin = serializer.validated_data.get('pin')
        
        try:
            user_pin = Pin.objects.get(user=user)
        except Pin.DoesNotExist:
            return CustomErrorResponse(message="User has not set up pin yet", status=400)
        
        if compare_word(user_pin.pin, str(pin)):
            return CustomSuccessResponse(message=True)
        else:
            return CustomErrorResponse(message=False)

class ChangePin(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePinSerializer

    def post(self, request):
        serializer = ChangePinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        old_pin = serializer.validated_data.get('old_pin')
        new_pin = serializer.validated_data.get('new_pin')
        
        try:
            user_pin = Pin.objects.get(user=user)
        except Pin.DoesNotExist:
            return CustomErrorResponse(message="User has not set up pin yet", status=400)
        
        if compare_word(user_pin.pin, str(old_pin)):
            hashed_pin = hashword(str(new_pin))
            user_pin.pin = hashed_pin
            user_pin.save()
            return CustomSuccessResponse(message="Successfully changed")
        else:
            return CustomErrorResponse(message="Old pin is incorrect")
        
# class UpdateKYCStatus(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = KYCSerializer

#     def post(self, request):
#         serializer = KYCSerializer(data=request.data)
#         if(serializer.is_valid()):
#             serializer.save()
#             return CustomSuccessResponse(message="successful")
#         else:
#             errors = serializer.errors
#             message = ""
#             for i in errors:
#                 message += errors[i][0]
#             message = message.replace('custom', '').strip().capitalize()
#             return CustomErrorResponse(message =message, status=status.HTTP_400_BAD_REQUEST)
class UpdateKYCStatus(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KYCSerializer

    def post(self, request):
        # Ensure only the has_kyc field is passed to the serializer
        data = {'has_kyc': request.data.get('has_kyc')}
        
        serializer = KYCSerializer(data=data)
        if serializer.is_valid():
            try:
                # Save the updated KYC status
                serializer.save()
                return CustomSuccessResponse(message="KYC update successful")
            except IntegrityError as e:
                # Handle IntegrityError specifically, e.g., if phone number is involved somehow
                return CustomErrorResponse(message="There was an issue with the update.", status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = serializer.errors
            message = ""
            for i in errors:
                message += errors[i][0]
            message = message.replace('custom', '').strip().capitalize()
            return CustomErrorResponse(message=message, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMainSerializer

    def get(self, request):
        user = request.user
        serializer = UserMainSerializer(user).data
        return CustomSuccessResponse(data=serializer)


 





class EnableTwoFactorAuthView(GenericAPIView):

    """
    API to enable two-factor authentication for the user.

    This API allows authenticated users to enable 2FA by sending an OTP
    to their email or phone number based on the selected two-factor type.

    Request Body:
        - two_factor_type: (str) The type of two-factor authentication ("email" or "phone_number").
    
    Response:
        - 200: OTP sent successfully.
        - 400: Invalid input or failed request.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TwoFactorAuthSerializerRequest


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not isinstance(user, CustomUser):
            raise ValueError(f"Expected CustomUser instance but got {type(user).__name__}")
        if not user.email:
            raise serializers.ValidationError("User email is required for email-based 2FA.")

        # Generate and send OTP
        otp = get_and_save_otp(user.email, length=4)
        cache.set(f"otp_{user.id}", otp, timeout=300)

        if serializer.validated_data["two_factor_type"] == "email":
            send_2fa_enable_mail(user, otp)
        elif serializer.validated_data["two_factor_type"] == "phone_number":
            send_sms(
                user.phone_number,
                f"Your KYC enable OTP is: {otp}. It will expire in 5 minutes."
            )

        user.two_factor_type = serializer.validated_data["two_factor_type"]
        user.save()

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle the POST request to enable two-factor authentication.

    #     Validates the request payload and sends an OTP to the user's
    #     selected two-factor type (email or phone number).

    #     Returns:
    #         - Success response with a message indicating that the OTP was sent.
    #         - Error response if the request payload is invalid.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     user = request.user
    #     two_factor_type = serializer.validated_data["two_factor_type"]

    #     # Generate OTP
    #     # otp = generate_otp()
    #     otp = get_and_save_otp(user.email, length=4)

    #     cache.set(f"otp_{user.id}", otp, timeout=300)  # Save OTP for 5 minutes

    #     # Send OTP
    #     if two_factor_type == "email":
    #         send_2fa_enable_mail(user.email, otp)
            
    #     elif two_factor_type == "phone_number":
    #         # send_otp_via_sms(user.phone_number, otp)
    #         send_sms(
    #             user.phone_number,
    #             f"Your KYC enable OTP is: {otp}. It will expire in 5 minutes."
    #         )

    #     user.two_factor_type = two_factor_type
    #     user.save()
    #     return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

    #     # return Response({"message": "OTP sent successfully."})

class VerifyOTPView(GenericAPIView):
    """
    API to verify the OTP and enable two-factor authentication for the user.

    This API allows authenticated users to verify the OTP sent via email
    or phone number. Upon successful verification, two-factor authentication
    is enabled for the user.

    Request Body:
        - otp: (str) The OTP received by the user.

    Response:
        - 200: 2FA enabled successfully.
        - 400: Invalid or expired OTP.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyOTPSerializer2fa
    # serializer_class = TwoFactorAuthSerializerRequest
    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to verify the OTP.

        Validates the OTP provided by the user. If the OTP is valid, two-factor
        authentication is enabled for the user. If the OTP is invalid or expired,
        an error response is returned.

        Returns:
            - Success response with a message indicating that 2FA is enabled.
            - Error response if the OTP is invalid or expired.
        """
        otp = request.data.get("otp")
        user = request.user

        if not otp:
            return CustomErrorResponse(
                message="OTP is required",
                status=status.HTTP_400_BAD_REQUEST,
            )

            # return Response({"error": "OTP is required."}, status=400)

        # Check OTP
        cached_otp = cache.get(f"otp_{user.id}")
        if cached_otp and str(cached_otp) == str(otp):
            user.two_factor_enabled = True
            user.save()
            cache.delete(f"otp_{user.id}")
           
            return  CustomSuccessResponse(
                
                message="2FA enabled successfully",
            )

        return CustomErrorResponse(
            message="Invalid or expired PIN code",
            status=status.HTTP_400_BAD_REQUEST,
        )