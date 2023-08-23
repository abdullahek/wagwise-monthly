# from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from flask.cli import FlaskGroup
from glogic import app, db, prepare_app, parser, models

prepare_app(environment='ms')
# migrate = Migrate(app, db)

cli = FlaskGroup(app)
# migrate.add_command('db', MigrateCommand)

@cli.command
def dbseed():

    # with open('dbseeding/registration.json') as survey_file:
    #     for i in parser.questions_parse(survey_file.read(), models.RegistrationQuestions):
    #         db.save(i)

    # with open('dbseeding/baseline.json') as survey_file:
    #     for i in parser.questions_parse(survey_file.read(), models.BaselineQuestions):
    #         db.save(i)

    with open('dbseeding/monthly.json') as survey_file:
        for i in parser.questions_parse(survey_file.read(), models.MonthlyQuestions):
            db.save(i)


if __name__ == "__main__":
    app.jinja_env.cache = {}
    cli()
