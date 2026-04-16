from flask import Flask, render_template, url_for, redirect, jsonify, request, Response, session
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/financeappdb"
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,server_default=db.func.now())
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            "email" : self.email,
            "user_name" : self.user_name,
            "created_at" : self.created_at
        }
    
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.Date, nullable=False, server_default=db.func.current_date())

    def to_dict(self):
        return {
            "name" : self.name,
            "date_added" : self.date_added
        }

class Expense(db.Model):
    __tablename__ = 'expense'
    transaction_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.category_id'), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)


@app.route('/sample',methods=['GET'])
def sample():
    results = User.query.all()
    # return results
    return jsonify([user.to_dict() for user in results])
    pass
    # return "This is a sample route"

@app.route('/')
def home():
    # return redirect(url_for('expense'))
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = data.get('username')
        password = data.get('password')
        try:
            user = User.query.filter_by(user_name=user).first()
            if not user or (user and not check_password_hash(user.password, password)):
                return jsonify({"message": "Invalid username or password"}), 401
            
            session.clear()
            session['username'] = user.user_name
            return jsonify({"message": "Login successful"}), 200
            # add logic for audit table and adding session management
        except Exception as e:
            print(f"Error occurred during login: {e}")
            return jsonify({"message": "An error occurred"}), 500
    return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "POST":
        data = request.get_json()
        username  = data.get('username')
        email = data.get('email')
        password = data.get('password')
        hashed_password = generate_password_hash(password)
        new_user = User(user_name=username, email=email, password=hashed_password)
        try:
            if User.query.filter_by(email=email).first():
                return jsonify({"message": "Email already exists"}), 400
            elif User.query.filter_by(user_name=username).first():
                return jsonify({"message": "Username already exists"}), 400
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while registering user: {e}")
            return jsonify({"message": "An error occurred"}), 500
       
        
        return jsonify({"message": "User registered successfully"}),200
        # add logic for audit table
      
    
    return render_template('signup.html')


@app.route('/forget-password')
def forget_password():
    return render_template('forget-password.html')

@app.route('/expense')
def expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('expense.html')

@app.route('/category', methods=['GET', 'POST'])
def category():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session.get('username')
    try:
        user = User.query.filter_by(user_name=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        categories = Category.query.filter_by(user_id=user.user_id).all()
    except Exception as e:
        print(f"Error occurred while displaying categories: {e}")
        return jsonify({"message": "An error occurred"}), 500
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        date = data.get('date') or db.func.now()
        try:
            category_exists = Category.query.filter_by(name=name, user_id=user.user_id).first()
            if category_exists:
                return jsonify({"message": "Category already exists"}), 400
            new_category = Category(name=name,date_added=date,user_id=user.user_id)
            db.session.add(new_category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while adding category: {e}")
        return jsonify({"message": "Category added successfully"}), 200
    
    return render_template('category.html',categories=categories)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    # Logout logic here

if __name__ == '__main__':
  
    app.run(debug=True)