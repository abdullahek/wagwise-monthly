from . import app, db
from .gresponses import Dictionary
from .models import Responses, User
from flask import request, session
from twilio.twiml.messaging_response import MessagingResponse
from bulk_sending.sql_stuff import validate_num, update_response

@app.route('/message', methods=['GET', 'POST'])
def bot():
    resp = MessagingResponse()
    user_input = request.form.get('Body').lower()
    num = request.form.get('From').replace('whatsapp:+', '')
    yes_no=""
    call_data=""
    if user_input in ["1", "2"]:
        resp.message("Great! Thank you for agreeing to participate. Keep an eye out in September." if user_input == "1" else "We are sorry to hear that. It will only take a few minutes and will earn you R125.")
        yes_no = "Yes" if user_input == "1" else "No"
        resp.message("We would also like to speak to you about how the WageWise programme has changed how you manage your money.\n\nIf you are willing to speak to us, please send a.\nIf you would prefer not to receive a call, send b.")
    elif user_input in ["a", "b"]:
        resp.message("Thank you for your response.")
        call_data = "Yes" if user_input == "a" else "No"
    else:
        resp.message("Please enter a valid response 1 or 2")
        yes_no = "invalid"

    if validate_num(num):
        update_response(yes_no, call_data if user_input in ['a', 'b'] else "", num)
    else:
        print("Number is not validated")

    return str(resp)
