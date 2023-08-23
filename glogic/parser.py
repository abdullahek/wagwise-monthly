import json


# parsers for seeding the database, called from manager
def questions_parse(json_string, db_table):
    questions = []
    questions_dicts = json.loads(json_string).get('questions')

    for question_dict in questions_dicts:
        # print(question_dict["num_ans"])
        body = question_dict['body']
        num_ops = question_dict['num_ans']
        questions.append(db_table(content=body, num_ops=num_ops))
    return questions
