import os
from dotenv import load_dotenv
from pathlib import Path


basedir = Path(__file__).parent
load_dotenv(basedir / '.env')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'
    SERVER_NAME = 'localhost:5000'

    # Dev only so browser doesnt cache for CSS
    if (os.environ.get('FLASK_ENV') == 'development'):
        SEND_FILE_MAX_AGE_DEFAULT = 0
    # auto reload template without needing to restart Flask
    TEMPLATES_AUTO_RELOAD = True

    #####

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # recommended by Pythonanywhere otherwise you get mysql timeout
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sendgrid settings
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_FROM = os.environ.get('MAIL_FROM')
    MAIL_ADMINS = os.environ.get('MAIL_ADMINS').split(' ')
    
    #####

    # DASHBOARD specific
    FORGOT_PASSWORD_TOKEN_EXPIRE = 3600  # in seconds, 3600 = 1 hour

    # POST specific
    # number of blog posts to show per page
    POSTS_PER_PAGE = 6
    # admin number of images
    IMAGES_PER_PAGE = 12
    SEARCH_RESULTS_RETURN = 12

    # CONTACT specific
    MESSAGES_PER_PAGE = 10

    # PAGE specific
    PAGES_PER_PAGE = 10
    UPLOAD_PATH_PAGE = basedir / 'app/static/uploads/page'
    UPLOAD_PATH_THUMB_PAGE = basedir / 'app/static/uploads/page/thumbnails'


