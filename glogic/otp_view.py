from flask import session, request
from twilio.twiml.messaging_response import MessagingResponse

from glogic import app, db
from glogic.models import User
from bulk_sending.template_send import delete_user_from_airtime_list
from .get_new_number_view import valid_num
from .correct_number_view import generate_random_string
from twilio.rest import Client
import os


@app.route('/otp', methods=["GET", "POST"])
def otp():
    """
    Collects and checks otp for airtime changes
    :return:
    """
    session['view'] = 'otp'

    response = MessagingResponse()

    num = request.form.get('From')
    num = num.replace('whatsapp:', '')
    incoming_msg = request.form.get('Body').lower()
    user = User.query.filter(User.number == num).first()

    if str(incoming_msg) == session['otp']:
        response.message("Thank you, the one-time pin you entered was correct and your phone number has been saved on our system. If you have any more issues receiving your airtime please contact digital@genesis-analytics.com and someone will help you. We look forward to hearing the rest of your survey responses.")
        print(num)
        user = User.query.filter(User.number == num).first()
        print(f"User ID: {user.id}")
        if session['airtime_num']:
            user.airtime_number = session['airtime_num']
        else:
            user.airtime_number = num
        db.session.commit()

        delete_user_from_airtime_list(num)
        del session['view']
        del session['otp']
    elif valid_num(incoming_msg):
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
    else:
        response.message("The OTP you entered was incorrect and so we are unable to update your details. Please contact digital@genesis-analytics.com to resolve this issue.")
        del session['view']
        del session['otp']
    return str(response)