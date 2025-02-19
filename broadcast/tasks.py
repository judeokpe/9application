from django.core.mail import send_mail
from account.models import CustomUser
from common.utils import send_template_email
from common.utils import send_sms
import threading
from django.core.mail import send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string
class EmailBroadcastThread(threading.Thread):
    def __init__(self, message, subject):
        self.message = message
        self.subject = subject
        threading.Thread.__init__(self)
    
    def run(self) -> None:
        email_broadcast(self.message, self.subject)
        return super().run()
class SMSBroadcastThread(threading.Thread):
    def __init__(self, message):
        self.message = message
        threading.Thread.__init__(self)
    
    def run(self) -> None:
        sms_broadcast(self.message)
        return super().run()

def email_broadcast(message='', subject=''):
    """
    send an email to all customers
    """    
    print('DISTRIBUTING EMAILS')
    emails = CustomUser.objects.all().values_list('email', flat=True)
    for email in emails:
        send_template_email('broadcast.html', email, subject, **{
            'message': message,
            'email_subject': subject
        },)
    
    print('Email distribution success')
    return True


def sms_broadcast(message=""):
    """
    send a text message to all customers
    """
    phone_numbers = CustomUser.objects.all().values_list('phone_number', flat=True)

    for phone_number in phone_numbers:
        if phone_number and phone_number != '':
            send_sms(phone_number, message)
    return True
    