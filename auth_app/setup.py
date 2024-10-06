from flask import Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy

# import requests
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv, path

# load env variables
load_dotenv()

db = SQLAlchemy()

base_dir = path.abspath(path.dirname(__name__))
db_path = path.join(base_dir, getenv('DATABASE_NAME'))

def create_auth_bp():
    auth_bp = Blueprint(
        "auth_bp", 
        __name__, 
        static_folder='static', 
        template_folder='templates')

    # db.init_app(auth_bp)
    
    # Enabling cross-origin requests
    cors = CORS()
    cors.init_app(auth_bp)

    
    db = current_app.extensions['sqlalchemy'].db

    return auth_bp, db
