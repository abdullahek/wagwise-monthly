from . import app, db
from .gresponses import Dictionary
from .models import Responses, User
from flask import request, session, url_for
from twilio.twiml.messaging_response import MessagingResponse
from bulk_sending.template_send import check_user_in_airtime_list
from bulk_sending.sql_stuff import validate_num
from bulk_sending.sql_stuff import update_response
import time

@app.route('/message', methods=['GET', 'POST'])
def bot():

    # for testing
    # del session['view']
    # del session['otp']
    # del session['question_id']
    # del session['count']


    resp = MessagingResponse()
    resp_start=request.form.get('Body').lower()
    yes_no=""
    call_data=""
    if resp_start=="1":
        yes_no="Yes"
        resp.message("Great! Thank you for agreeing to participate. Keep an eye out in September.")
        time.sleep(1)
        resp.message("We would also like to speak to you about how the WageWise programme has changed how you manage your money.\n\nIf you are willing to speak to us, please send a.\nIf you would prefer not to receive a call, send b. ")
    elif resp_start=="2":
        yes_no="No"
        resp.message("We are sorry to hear that. It will only take a few minutes and will earn you R125. If you change your mind, look out for the opportunity to earn in September.")
        time.sleep(1)
        resp.message("We would also like to speak to you about how the WageWise programme has changed how you manage your money.\n\nIf you are willing to speak to us, please send a.\nIf you would prefer not to receive a call, send b. ")
    elif resp_start=="a":
        call_data="Yes"
        resp.message("Thank you for your response.")
    elif resp_start=="b":
        call_data="No"
        resp.message("Thank you for your response.")
    else:
        yes_no="invalid response"
        resp.message("Please enter a valid response 1 or 2")
    num = request.form.get('From')
    num = num.replace('whatsapp:+', '')
    incoming_msg = request.form.get('Body').lower()
    print("INCOMING MSG: " + yes_no)
    result = validate_num(num) 
    if result:
        # resp.message("Thank you! Number is validated")
        response= update_response(yes_no,call_data, num)
    else: 
        print("Number is not validated")
              
    
    return str(resp)    
