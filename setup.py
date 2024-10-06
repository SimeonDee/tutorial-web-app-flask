from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

base_dir = path.abspath(path.dirname(__name__))
db_path = path.join(base_dir, getenv('DATABASE_NAME'))

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{getenv("DATABASE_NAME")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initializing db
    db.init_app(app)

     # Enabling cross-origin requests
    cors = CORS()
    cors.init_app(app)

    return app

