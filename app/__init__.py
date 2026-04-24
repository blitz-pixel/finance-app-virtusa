from flask import Flask, request, jsonify, session
import os
from dotenv import load_dotenv
from datetime import timedelta

from .extensions import db
from .routes import register_routes

def create_app():
    load_dotenv()
    app = Flask(__name__)

    database_uri = os.getenv('DATABASE_URI')
    secret_key = os.getenv('SECRET_KEY')
    flask_env = os.getenv("FLASK_ENV", "production")


    if not database_uri and flask_env == "production":
        database_uri = "mysql+pymysql://root:1234@localhost/financeappdb"
    
    if not database_uri:
        return ValueError("Missing database URI in environment variable")
    
    if not secret_key:
        return ValueError("Missing secret key in environment variable")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SECRET_KEY"] = secret_key
    # app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)

    # @app.before_request
    # def session_timeout():
    #     if request.endpoint == 'static':
    #         return
    #     session.permanent = True
       
    db.init_app(app)
    
    register_routes(app)
    return app