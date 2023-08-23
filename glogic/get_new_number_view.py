import os

from flask import session, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import re
from glogic import app, db
import random
import string


@app.route('/get_new_number', methods=["GET", "POST"])
def get_new_number():
    session['view'] = 'get_new_number'
    response = MessagingResponse()

    num = request.form.get('From')
    num = num.replace('whatsapp:', '')
    incoming_msg = request.form.get('Body').lower()

    if valid_num(incoming_msg):
        session['otp'] = generate_random_string(5)


        # Your Twilio account SID and auth token
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        # Your Twilio phone number and the destination phone number
        from_phone = "+27600185052"
        to_phone = f"+27{incoming_msg[1:]}"

        # Create the Twilio client
        client = Client(account_sid, auth_token)

        # Send the SMS message
        message = client.messages.create(
            body=f'Your one-time pin for the Wage Wise survey is {session["otp"]}. Please respond in the WhatsApp chat with this pin only.',
            from_=from_phone,
            to=to_phone
        )
        print(message.sid)
        print(session["otp"])

        response.message(
            f"A one-time pin has been sent to {incoming_msg}. Please respond to this message with that pin only. If " +
            "the phone number the pin was sent to is incorrect, please reply with only the phone number in the " +
            "correct format.")
        session['airtime_num'] = to_phone
        session['view'] = 'otp'

    else:
        response.message(
            "The phone number you entered is not in a format I can understand. \n\nPlease respond with the 10 digit phone number you would like your airtime sent to in the format 0123456789.")
    return str(response)


def valid_num(number):
    pattern = r'^0\d{9}$'
    if re.match(pattern, number):
        return True
    else:
        return False



def generate_random_string(length):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(length))

