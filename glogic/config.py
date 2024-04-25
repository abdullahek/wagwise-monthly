import os
import urllib.parse
# noinspection PyUnresolvedReferences


server = os.environ.get('SERVER')
database = os.environ.get('DATABASE')
username = os.environ.get('NAME')
password = os.environ.get('PASSWORD')


params = urllib.parse.quote_plus("DRIVER={ODBC Driver 18 for SQL Server};SERVER=" + server + ';DATABASE=' + database +
                                 ";UID=" + username + ';PWD=' + password)



class MSSQLConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                               os.path.join(basedir, 'test.sqlite'))
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True


config_env_files = {
    'ms': 'glogic.config.MSSQLConfig',
    'test': 'glogic.config.TestConfig'
}
