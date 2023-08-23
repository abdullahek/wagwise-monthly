from datetime import datetime

from sqlalchemy.ext.automap import automap_base

from . import db

Base = automap_base()


class BaselineQuestions(db.Model):
    __tablename__ = 'baseline_questions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    num_ops = db.Column(db.Integer, nullable=False)
    answers = db.relationship("BaselineAnswers", backref='question', lazy='dynamic')

    def __init__(self, content, num_ops):
        self.content = content
        self.num_ops = num_ops

    def next(self):
        return self.query.filter(BaselineQuestions.id > self.id) \
            .order_by('id').first()

class MonthlyQuestions(db.Model):
    __tablename__ = 'monthly_questions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    num_ops = db.Column(db.Integer, nullable=False)
    answers = db.relationship("MonthlyAnswers", backref='question', lazy='dynamic')

    def __init__(self, content, num_ops):
        self.content = content
        self.num_ops = num_ops

    def next(self):
        return self.query.filter(MonthlyQuestions.id > self.id) \
            .order_by('id').first()



class BaselineAnswers(db.Model):
    __tablename__ = 'baseline_answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('baseline_questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, question, user):
        self.content = content
        self.question = question
        self.user = user



class MonthlyAnswers(db.Model):
    __tablename__ = 'monthly_answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('monthly_questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    month = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now, nullable=True)

    def __init__(self, content, question, user, month):
        self.content = content
        self.question = question
        self.user = user
        self.month = month

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True)
    number_2 = db.Column(db.String, unique=True)
    registered = db.Column(db.Integer, default=0)
    last_month_completed = db.Column(db.Integer, default=0)
    airtime_number = db.Column(db.String, unique=True)

    baseline = db.relationship("BaselineAnswers", backref='user', lazy='dynamic')
    monthly = db.relationship("MonthlyAnswers", backref='user', lazy='dynamic')

    def __init__(self, number, number_2):
        self.number = number
        self.number_2 = number_2


class Responses(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    question_1 = db.Column(db.Integer, default=0)
    question_2 = db.Column(db.Integer, default=0)
    question_3 = db.Column(db.Integer, default=0)
    date_completed = db.Column(db.DateTime, nullable=True)

    def __init__(self, number, question_1=0, question_2=0, question_3=0):
        self.number = number
        self.month = int(datetime.now().month)
        self.question_1 = question_1
        self.question_2 = question_2
        self.question_3 = question_3
        self.date_completed = datetime.now()
        
