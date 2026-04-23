from flask import Flask, render_template, url_for, redirect, jsonify, request, Response, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
from  werkzeug.security import generate_password_hash, check_password_hash
import os
# from datetime import datetime
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
    expenses = db.relationship('Expense', backref='category', lazy=True)

    def to_dict(self):
        return {
            "name" : self.name,
            "date_added" : self.date_added
        }

class Expense(db.Model):
    __tablename__ = 'transaction'
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
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = data.get('username')
        password = data.get('password')
        try:
            session.clear()
            user_username = User.query.filter_by(user_name=user).first()
            user_email = User.query.filter_by(email=user).first()
            user_valid = user_username or user_email
            if not user_valid or (user_valid and not check_password_hash(user_valid.password, password)):
                return jsonify({"message": "Invalid username or password"}), 401
            
            session['username'] = user_valid.user_name
            return jsonify({"message": "Login successful"}), 200
    
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
            db.session.flush()
            new_categories = [
                Category(name="Housing", user_id = new_user.user_id),
                Category(name="Entertainment", user_id = new_user.user_id),
                Category(name="Education", user_id = new_user.user_id),
                Category(name="Transportation", user_id = new_user.user_id),
                Category(name="Gifts & Donations", user_id = new_user.user_id),
                Category(name="Miscellaneous", user_id = new_user.user_id)
            ]
            db.session.add_all(new_categories)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while registering user: {e}")
            return jsonify({"message": "An error occurred"}), 500
       
        
        return jsonify({"message": "User registered successfully"}),200
     
      
    
    return render_template('signup.html')

@app.route('/expense',methods=['GET', 'POST','DELETE'])
def expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session.get('username')
    try:
        user = User.query.filter_by(user_name=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        # categories = Category.query.filter_by(user_id=user.user_id).all()
    except Exception as e:
        print(f"Error occurred while displaying categories: {e}")
        return jsonify({"message": "An error occurred"}), 500
    if request.method == 'POST':
        data = request.get_json()
        category = data.get('category')
        amount = data.get('amount')
        if int(amount) < 0:
            return jsonify({"message": "Amount cannot be negative"}), 400
        elif int(amount) > 999999999:
            return jsonify({"message": "Amount exceeds maximum limit"}), 400
        date = data.get('date') or db.func.now()
        description = data.get('description')
        category_id = Category.query.filter_by(name=category, user_id=user.user_id).first().category_id
        new_expense = Expense(category_id=category_id, amount=amount, date=date, description=description, user_id=user.user_id)
        try:
            db.session.add(new_expense)
            db.session.flush()
            new_date = new_expense.date.strftime("%Y-%m-%d %H:%M:%S")
            transaction_id = new_expense.transaction_id
            db.session.commit()
            return jsonify({"message": "Expense added successfully", "date" : new_date, "transaction_id" : transaction_id}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while adding expense: {e}")
            return jsonify({"message": "An error occurred"}), 500
    elif request.method == 'DELETE':
        expense_id = request.args.get('expense_id')
        try:
            db.session.query(Expense).filter(Expense.transaction_id == expense_id).delete()
            db.session.commit()
            return jsonify({"message": "Expense deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while deleting expense: {e}")
            return jsonify({"message": "An error occurred"}), 500

    
    try:
        categories = Category.query.filter_by(user_id=user.user_id).all()
        expenses = Expense.query.filter_by(user_id=user.user_id).all()
    except Exception as e:
        print(f"Error occurred while displaying categories: {e}")
        return jsonify({"message": "An error occurred"}), 500
    print(categories)
    return render_template('expense.html',categories=categories, expenses=expenses, username=username)

@app.route('/category', methods=['GET', 'POST', 'DELETE'])
def category():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session.get('username')
    try:
        user = User.query.filter_by(user_name=username).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
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
            db.session.flush()
            new_date = new_category.date_added
            db.session.commit()
            return jsonify({"message": "Category added successfully", "date": new_date}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while adding category: {e}")
            return jsonify({"message": "An error occurred"}), 500
    elif request.method == 'DELETE':
        category_id = request.args.get('category_id')
        try:
            db.session.query(Category).filter(Category.category_id == category_id, Category.user_id == user.user_id).delete()
            db.session.commit()
            return jsonify({"message": "Category deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while deleting category: {e}")
            return jsonify({"message": "An error occurred"}), 500
    try:
        categories = Category.query.filter_by(user_id=user.user_id).all()
    except Exception as e:
        print(f"Error occurred while displaying categories: {e}")
        return jsonify({"message": "An error occurred"}), 500
  

    return render_template('category.html',categories=categories)

@app.route('/report', methods=['GET', 'POST'])
def report():
    username = session.get('username')
    user = User.query.filter_by(user_name=username).first()
    if not user:
        return redirect(url_for('login'))

    categories = [
        category.name
        for category in Category.query.filter_by(user_id=user.user_id).order_by(Category.name).all()
    ]

    if request.method == 'POST':
        monthly_totals = (
            db.session.query(
                extract('year', Expense.date).label('year'),
                extract('month', Expense.date).label('month'),
                func.coalesce(func.sum(Expense.amount), 0).label('totalAmount'),
            )
            .filter(Expense.user_id == user.user_id)
            .group_by(
                extract('year', Expense.date),
                extract('month', Expense.date),
            )
            .order_by(
                extract('year', Expense.date),
                extract('month', Expense.date),
            )
            .all()
        )

        yearly_totals = (
            db.session.query(
                extract('year', Expense.date).label('year'),
                func.coalesce(func.sum(Expense.amount), 0).label('totalAmount'),
            )
            .filter(Expense.user_id == user.user_id)
            .group_by(extract('year', Expense.date))
            .order_by(extract('year', Expense.date))
            .all()
        )

        monthly_category_totals = (
            db.session.query(
                Category.name.label('category_name'),
                extract('year', Expense.date).label('year'),
                extract('month', Expense.date).label('month'),
                func.coalesce(func.sum(Expense.amount), 0).label('totalAmount'),
            )
            .join(Category, Expense.category_id == Category.category_id)
            .filter(Expense.user_id == user.user_id)
            .group_by(
                Category.name,
                extract('year', Expense.date),
                extract('month', Expense.date),
            )
            .order_by(
                extract('year', Expense.date),
                extract('month', Expense.date),
                Category.name,
            )
            .all()
        )

        yearly_category_totals = (
            db.session.query(
                Category.name.label('category_name'),
                extract('year', Expense.date).label('year'),
                func.coalesce(func.sum(Expense.amount), 0).label('totalAmount'),
            )
            .join(Category, Expense.category_id == Category.category_id)
            .filter(Expense.user_id == user.user_id)
            .group_by(
                Category.name,
                extract('year', Expense.date),
            )
            .order_by(
                extract('year', Expense.date),
                Category.name,
            )
            .all()
        )

        return jsonify({"message" : "Data fetched successfully",
            "monthly_totals": [
                {
                    "year": int(row.year),
                    "month": int(row.month),
                    "totalAmount": float(row.totalAmount),
                }
                for row in monthly_totals
            ],
            "yearly_totals": [
                {
                    "year": int(row.year),
                    "totalAmount": float(row.totalAmount),
                }
                for row in yearly_totals
            ],
            "monthly_category_totals": [
                {
                    "category_name": row.category_name,
                    "year": int(row.year),
                    "month": int(row.month),
                    "totalAmount": float(row.totalAmount),
                }
                for row in monthly_category_totals
            ],
            "yearly_category_totals": [
                {
                    "category_name": row.category_name,
                    "year": int(row.year),
                    "totalAmount": float(row.totalAmount),
                }
                for row in yearly_category_totals
            ],
        }), 200

    return render_template('report.html', categories=categories)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    # Logout logic here

if __name__ == '__main__':
  
    app.run(debug=True)