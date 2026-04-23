from flask import session
from app.models import User,Category
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db


def login_user(username, password):
    # print(f"Attempting to log in user: {username}")
    try:
        if not username or not password:
            return {
                "message": "Username and password are required",
                "status_code": 400
            }
        session.clear()
        user_username = User.query.filter_by(user_name=username).first()
        user_email = User.query.filter_by(email=username).first()
        user_valid = user_username or user_email
        if not user_valid or (user_valid and not check_password_hash(user_valid.password, password)):
        
            
            return {
                "message": "Invalid username or password",
                "status_code": 401
            }
        
        
        session['username'] = user_valid.user_name
        return {
            "message": "Login successful",
            "status_code": 200
        }
    except Exception as e:
        print(f"Error occurred during login: {e}")
        return {
            "message": "An error occurred",
            "status_code": 500
        }
    
def signup_user(username, email, password):
        hashed_password = generate_password_hash(password)
        new_user = User(user_name=username, email=email, password=hashed_password)
        try:
            if User.query.filter_by(email=email).first():
                return {
                    "message": "Email already exists",
                    "status_code": 400
                }
            elif User.query.filter_by(user_name=username).first():
                return {
                    "message": "Username already exists",
                    "status_code": 400
                }
            db.session.add(new_user)
            db.session.flush()
            new_categories = create_categories(new_user.user_id)
           
            db.session.add_all(new_categories)
            db.session.commit()
            return {
                "message": "User registered successfully",
                "status_code": 200
            }
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while registering user: {e}")
            return {
                "message": "An error occurred",
                "status_code": 500
            }

def create_categories(user_id):
    default_categories = [
            Category(name="Housing", user_id = user_id),
            Category(name="Entertainment", user_id = user_id),
            Category(name="Education", user_id = user_id),
            Category(name="Transportation", user_id = user_id),
            Category(name="Gifts & Donations", user_id = user_id),
            Category(name="Miscellaneous", user_id = user_id)
        ]
    return default_categories
    

    