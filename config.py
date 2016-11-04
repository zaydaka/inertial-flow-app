import os
basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = basedir+"/database/"

class BaseConfig(object):
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'worker@inertialflow.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'InertAmerica1')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"NoReply" <worker@inertialflow.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "InertialFlow"                # Used by email templates
