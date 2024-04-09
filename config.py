from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['MAIL_SERVER']= os.getenv('EMAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('EMAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)
db = SQLAlchemy(app)



