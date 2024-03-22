import os
from dotenv import load_dotenv
load_dotenv()
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/testdb')
    SECRET_KEY = os.environ.get('SECRET_KEY', '123123')