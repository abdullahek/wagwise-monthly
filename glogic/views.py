from . import app
from .import bot_view, survey_view, baseline_view, correct_number_view, otp_view, get_new_number_view


@app.route('/', methods=['GET', 'POST'])
def root():
    return "I'm working"
