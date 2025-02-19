import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.conf import settings

def send_activation_email(user):
    """Generate OTP, store it in cache, and send activation email to the user."""
    email = user.email
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    cache.set(email, otp, timeout=300)

    send_mail(
        'OTP Code',
        f'Your OTP is: {otp}. This Code will expire in 5 minutes',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def send_activation_sms(user):
    """Generate OTP, store it in cache, and send activation SMS to the user."""
    phone_number = user.phone_number
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    cache.set(phone_number, otp, timeout=300)
    
    # Use Twilio to send the OTP via SMS
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # Option 1: Using Twilio's Messaging API
    message = client.messages.create(
        body=f'Your OTP is: {otp}. This Code will expire in 5 minutes',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    # Option 2: Using Twilio's Verify API (uncomment if you're using Verify service)
    verification = client.verify.v2.services('VA6bf79a55b613a4ba768a9db5be97c665').verifications.create(
        to=phone_number,
        channel='sms'
    )
