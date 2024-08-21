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


    num = request.form.get('From')
    num = num.replace('whatsapp:+', '')
    incoming_msg = request.form.get('Body').lower()

    print("INCOMING MSG: " + incoming_msg)

    resp = MessagingResponse()

    result = validate_num(num) 
    if result:
        # resp.message("Thank you! Number is validated")
        response= update_response(incoming_msg, num)
        resp.message("Thank you! Number is validated")
    else:
        
        resp.message("Number is not validated")
    
    
    if 'stop' in incoming_msg:
        resp.message("We will be sad to see you go.")
        user = User.query.filter(User.number==num).first()
        user.last_month_completed = 100
        db.session.commit()
        return str(resp)
    if 'part' in incoming_msg:
        resp.message("Thank You for Opting to  Participate in our Endline Survey!")
        return str(resp)

    if "view" in session:
        print("Redirect to: " + session['view'])
        resp.redirect(url_for(session["view"]))
    else:
        # for airtime corrections
        if check_user_in_airtime_list(num):
            out ="Hi! You have opted into the WageWise survey brought to you by Genesis Analytics. We understand that you have been having issues receiving your R17 airtime for completing the survey."
            out += " Please follow this simple process for us to verify your phone number and get your airtime to you.\n\n"
            out += f"You are messaging us from 0{num[3:]}. Is this the number you would like to receive your airtime on? Answer *yes* or *no*."

            session['view'] = 'correct_number'

        # main entry point for monthly surveys
        elif ('hi' in incoming_msg) or ('hello' in incoming_msg) or ('menu' in incoming_msg) or ('ok' in incoming_msg) or ("yes" in incoming_msg):

            reg = registered(num)
            if reg == 1:
                # survey starts
                session['view'] = 'survey'
                session['count'] = 0
                out = "Thank you for participating in the WageWise 3 year survey. " + Dictionary['welcome3']

            else:
                out = "Your phone number is not in our database. If you have participated in the WageWise program and completed the registration, please contact digital@genesis-analytics.com."


        elif ('are you still working' in incoming_msg):
            out = "Yes, all is well"
        elif ('part' in incoming_msg):
            out = "Thanks for your willing in the participation."

        
        else:
            out = f"I'm sorry, but there's been a problem. \
Please say \"Hi\" to try again."
        resp.message(out)

    return str(resp)


# checks to see if user is in DB and, if not, adds them
def user_error(num):
    if Responses.query.filter(Responses.number == num).first() is not None:
        return True

    return False

def registered(num):
    """
    Returns 0 if user is not registered, 1 if registered
    """
    user = User.query.filter(User.number == num).first()
    if user is not None:
        if user.registered == 1:
            return 1
        else:
            return 0
    else:
        return 0

