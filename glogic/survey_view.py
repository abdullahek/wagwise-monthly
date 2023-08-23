from datetime import datetime

from flask import request, session
from twilio.twiml.messaging_response import MessagingResponse

from . import app, db
from .models import MonthlyQuestions, MonthlyAnswers, User
from .send_airtime import send_airtime_after_survey


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    session['view'] = 'survey'
    """
    Redirect for the survey view. Holds survey logic.
    :return str: response
    """
    num = request.form.get('From')
    num = num.replace('whatsapp:', '')

    incoming_msg = request.form.get('Body').lower()
    resp = MessagingResponse()

    if 'question_id' in session:


        return answers(session['question_id'], resp, num)
    else:
        if user_error(num) == 1:
            mydate = datetime.now()
            mon = mydate.strftime("%B")
            resp.message(f"Our records indicate that you have already completed the survey for {mon}. We look forward to hearing from you next month.")
            del session['view']
            del session['count']
            return str(resp)
        if user_error(num) == 2:
            resp.message("Our records indicate that you did not complete the registration. Consequently, you will not be able to participate in the monthly questionairre.")
            del session['view']
            del session['count']
            return str(resp)
        else:
            first_question = redirect_to_first_question(resp)
            resp.message(first_question.content)
    return str(resp)

def answers(question_id, response, num):
    question = MonthlyQuestions.query.get(question_id)

    incoming_msg = request.form.get('Body').lower()

    # multi select for all

    if question_id == 4 or question_id == 6 or question_id== 7:
        if len(incoming_msg) > 1:
            response.message("Your answer is invalid. Please select _one_ option that is most true for you.")
            return str(response)

    for i in incoming_msg:
        if i == " " or i == ',':

            continue
        else:
            try:
                int(i)

            except ValueError:
                response.message(
                    "Please respond with the number of your response. Separate multiple options with a space or a comma only.")
                return str(response)
            else:
                if int(i) > question.num_ops:
                    response.message("Your answer is invalid. Please respond with one or more of the given options.")
                    return str(response)

    db.save(MonthlyAnswers(content=incoming_msg,
                             question=question,
                             user=User.query.filter(User.number == num).first(),
                             month=((int(datetime.now().year) - 2022)*12) +  (int(datetime.now().month) - 8)))
    session['count'] += 1

    next_question = question.next()

    if next_question and session['count'] < 3:
        response.message(questions(next_question.id))

    else:
        user = User.query.filter(User.number == num).first()
        user.last_month_completed = ((int(datetime.now().year) - 2022)*12) +  (int(datetime.now().month) - 8)
        db.session.commit()
        airtime = send_airtime_after_survey(user.airtime_number, 17)
        # airtime = 0

        response.message("Thank you for completing the survey. Your R17 is on its way to you now. If " \
"you have not received your airtime or you would like to give feedback for the bot, please contact digital@genesis-analytics.com")

        del (session['question_id'])
        del session["view"]
        del session["count"]

    return str(response)


def questions(question_id):
    question = MonthlyQuestions.query.get(question_id)
    session['question_id'] = question.id
    return question.content


# goes to question view and finds first question
def redirect_to_first_question(response):
    current_month = ((int(datetime.now().year) - 2022)*12) +  (int(datetime.now().month) - 8)

    # for running every 3 months
    starting_q_mo = current_month % 3

    if starting_q_mo == 1:
        starting_q = 1
    elif starting_q_mo == 2:
        starting_q = 4
    else:
        starting_q = 7

    session['question_id'] = starting_q

    return MonthlyQuestions.query.filter(MonthlyQuestions.id == starting_q).first()


# checks to see if user is in DB and has not completed current month
def user_error(num):
    user = User.query.filter(User.number == num).first()
    if user is None:
        return 2
    if user is not None:
        current_month = ((int(datetime.now().year) - 2022)*12) +  (int(datetime.now().month) - 8)
        if user.last_month_completed >= current_month:
            return 1
        if user.registered !=1:
            return 2
    return -1