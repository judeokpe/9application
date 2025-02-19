import logging
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
from datetime import timedelta



def get_first_error(errors):
    """
    Gets the first message in a serializer.errors
    
    Parameters:
    errors: The error messages of a serializer i.e serializer.errors
    """
    field, error_list = next(iter(errors.items()))
    return str(error_list[0])

# Logger setup
logger = logging.getLogger(__name__)

# Function definitions
def generate_code(length=5):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def get_expiration_time():
    return int(5)

def get_and_save_otp(phone_or_email, length=5, timeout=300):
    otp = generate_code(length)
    cache.set(phone_or_email, otp, timeout)
    return otp

def send_activation_email(user):
    """Generate OTP, store it in cache, and send activation email to the user."""
    otp = get_and_save_otp(user.email)
    send_mail(
        'OTP Code',
        f'Your OTP is: {otp}. This code will expire in 5 minutes.',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

def send_activation_sms(user):
    """Generate OTP, store it in cache, and send activation SMS to the user."""
    otp = get_and_save_otp(user.phone_number)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}. It will expire in 5 minutes.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=user.phone_number,
    )

def send_sms(phone_number, body):
    """Send an SMS to a phone number."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number,
    )

def send_verify_sms(phone_number, body):
    """Send a verification SMS using Twilio's Verify service."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(
        to=phone_number, custom_message=body, channel='sms'
    )

def send_template_email(template, email, subject, **context):
    """Send an email based on a template."""
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        f"9app <{settings.EMAIL_HOST_USER}>",
        [email],
        html_message=html_message,
    )


# def get_expiration_time():
#     # Define the expiration time for the OTP in minutes
#     expiration_minutes = 5  # Set to 10 minutes, or adjust as required
#     return expiration_minutes

def send_reset_request_mail(user, verification_code):
    
    send_template_email(
        "password_reset.html",
        user.email,
        "Password Reset",
        **{
            "name": user.first_name + user.last_name,
            "verification_link": 'https://andromedia-api-64b890199b07.herokuapp.com/api/v1/auth/confirm_password/', #'http://127.0.0.1:8000/api/v1/auth/confirm_password/',
            "otp_code": verification_code,
            "expiration_time": get_expiration_time(),
        },
    )


def send_reset_request_sms(user, verification_code):
    # Prepare the SMS message content
    message_content = (
        f"9APP\n\n"
        f"Your password reset OTP is: {verification_code}.\n"
        f"It will expire in  {get_expiration_time()} minutes.\n\n"
        # f"Link to reset password: https://andromedia-api-64b890199b07.herokuapp.com/api/v1/auth/confirm_password/"
    )
    
    # Send the SMS using your SMS service provider (e.g., Twilio)
    try:        
        # Set up Twilio client (replace with your actual Twilio credentials)
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        
        # Send the message
        client.messages.create(
            body=message_content,
            from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
            to=user.phone_number   # User's phone number
        )
    except Exception as e:
        print(f"Error sending SMS: {e}")


def send_verify_mail(user, verification_code):
    
    send_template_email(
        "verify.html",
        user.email,
        "Verify your account",
        **{
            "name": user.first_name + user.last_name,
            "otp_code": verification_code,
            "expiration_time": get_expiration_time(),
        },
    )
def send_2fa_enable_mail(user, verification_code):
    
    send_template_email(
        "2fa.html",
        user.email,
        "Confirm two-factor authentication on  your account",
        **{
            "name": user.first_name + user.last_name,
            "otp_code": verification_code,
            "expiration_time": get_expiration_time(),
        },
    )
    
def send_subscribe_mail(user, plan):
    send_template_email(
        "subscribe.html",
        user.email,
        "Subscription successful",
        **{
            "name": user.first_name + user.last_name,
            "app_name": 'Andromeda',
            "subscription_plan_name": plan
        },
    )
    
def send_signup_mail(user):
    send_template_email(
        "signup.html",
        user.email,
        "Welcome Onboard",
        **{
            "name": user.first_name + user.last_name,
            "company_name": ""
        },
    )
    
# def send_widget_mail(company_name, user_id, widget):
#     user = CustomUser.objects.get(id=user_id)
#     send_template_email(
#         "send-widget.html",
#         user.email,
#         "Welcome Onboard",
#         **{
#             "name": user.name,
#             "company_name": company_name
#         },
#     )

# def send_add_team_mate_mail(email, company_id):
#     company = Company.objects.get(id=company_id)
#     send_template_email(
#         "addteammate.html",
#         email,
#         "Welcome Onboard",
#         **{
#             "teammate_name": 'teammate_name',
#             "company_name": company.name,
#             "login_url":'login_url'
#         },
#     )


def call_web3_service(path, data):
    # URL of your Flask web3 microservice
    url = 'https://web3.9app.co/'+path
    
    # Make a POST request
    response = requests.post(url, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Process the JSON response
    else:
        response.raise_for_status()  # Handle errors or raise exceptions


import requests
from django.conf import settings

def make_api_request(path, method='get', data=None, params=None):
    base_url = "https://web3.9app.co"
    url = f"{base_url}{path}"
    headers = {'Content-Type': 'application/json'}

    if method.lower() == 'get':
        response = requests.get(url, headers=headers, params=params)
    else:
        response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        return response.json()
    else:
        response.raise_for_status()


from argon2 import PasswordHasher

def hashword(word):
    ph = PasswordHasher()
    hashed = ph.hash(word)
    return hashed

def compare_word(hash, word):
    ph = PasswordHasher()
# To verify the password:
    try:
        ph.verify(hash, word)
        return True
    except:
        return False