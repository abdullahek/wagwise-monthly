from flask import session
from twilio.twiml.messaging_response import MessagingResponse

from .gresponses import Dictionary

def return_to_menu():
    """
    Main function is to remove 'View' from session. Returns user to menu
    :return str: out
    """
    out = Dictionary['welcome']
    if 'view' in session:
        del session['view']
    return out

def sms_twiml(question):
    response = MessagingResponse()
    response.message(question.content)
    return str(response)