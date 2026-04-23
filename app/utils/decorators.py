from functools import wraps
from flask import session, url_for, redirect, jsonify
from app.models import User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("auth.login"))
        
        username = session.get("username")
    
        user = User.query.filter_by(user_name=username).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        return f(user, *args, **kwargs)
    
    return decorated_function
