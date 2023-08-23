import os

from flask import session, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from glogic import app
import string
import random

@app.route('/correct_number', methods=["GET", "POST"])
def correct_number():
    """
    View for user correcting their airtime number.
    """
    session['view'] = 'correct_number'
    response = MessagingResponse()

    num = request.form.get('From')
    num = num.replace('whatsapp:', '')
    incoming_msg = request.form.get('Body').lower()


    if 'yes' in incoming_msg:
        session['otp'] = generate_random_string(5)


        # Your Twilio account SID and auth token
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        # Your Twilio phone number and the destination phone number
        from_phone = "+27600185052"
        to_phone = num

        # Create the Twilio client
        client = Client(account_sid, auth_token)

        # Send the SMS message
        message = client.messages.create(
            body=f'Your one-time pin for the Wage Wise survey is {session["otp"]}',
            from_=from_phone,
            to=to_phone
        )
        print(message.sid)
        print(session["otp"])

        response.message(
            f"A one-time pin has been sent to 0{num[3:]}. Please respond to this message with that one-time pin number only. If you do not receive a one-time pin after 5 minutes, please check if the phone number is correct. It must be a South African number and cannot be a whatsapp number only. If the phone number the pin was sent to is incorrect, please reply with only the phone number in the correct format (0{num[3:]}).")
        session['airtime_num'] = to_phone
        session['view'] = 'otp'



    elif "no" in incoming_msg:
        response.message("Please respond with the phone number you would like your airtime sent to in the format 0123456789. " +
                         "Please double check that the phone number is entered correctly.")
        session['view'] = 'get_new_number'


    else:
        response.message("I'm sorry, I do not understand your response. Please respond with yes/no.")


    return str(response)

def generate_random_string(length):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(length))


