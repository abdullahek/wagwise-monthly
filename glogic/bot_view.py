from . import app, db
from .gresponses import Dictionary
from .models import Responses, User
from flask import request, session, url_for
from twilio.twiml.messaging_response import MessagingResponse
from bulk_sending.template_send import check_user_in_airtime_list
from bulk_sending.sql_stuff import validate_num
from bulk_sending.sql_stuff import update_response


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
        resp.message("Great! Thank you for agreeing to participate!")
    elif resp_start=="2":
        yes_no="No"
        resp.message("Sad to hear that.")
    elif resp_start=="a":
        call_data="Yes"
    elif resp_start=="b":
        call_data="No"
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
    
