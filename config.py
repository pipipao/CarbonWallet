import os
import platform

DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'carbon_wallet'
USERNAME = 'root'
if platform.system() == 'Linux':
    PASSWORD = ''
else:
    print("当前为开发环境")
    PASSWORD = ''
DB_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD,
                                                                        HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
