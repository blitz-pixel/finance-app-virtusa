from flask import Blueprint, render_template, url_for, redirect, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User, Category
from app.services.auth_service import login_user, signup_user
from app.utils.decorators import login_required

auth_bp = Blueprint("auth", __name__)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()
            user = data["username"]
            password = data["password"]
            result = login_user(user, password)
            return jsonify({"message": result["message"]}), result["status_code"]
        except Exception as e:
            print(f"Error occurred during requesting login data: {e}")
            return jsonify({"message": str(e)}), 500
  
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        try:
            data = request.get_json()
            username = data["username"]
            email = data["email"]
            password = data["password"]
            result = signup_user(username, email, password)
            return jsonify({"message": result["message"]}), result["status_code"]
        except Exception as e:
            print(f"Error occurred during requesting signup data: {e}")
            return jsonify({"message": str(e)}), 500
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
    