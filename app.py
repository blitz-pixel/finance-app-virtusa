from flask import Flask, render_template, url_for, redirect, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/financeappdb"
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

@app.route('/login')
def login():
   
    return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    # print(request.method)
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
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred while checking email uniqueness"}), 500
       
        
        return jsonify({"message": "User registered successfully"}),200
        # add logic for audit table
      
    
    return render_template('signup.html')


@app.route('/forget-password')
def forget_password():
    return render_template('forget-password.html')

@app.route('/expense')
def expense():
    return render_template('expense.html')

@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/logout')
def logout():
    pass
    # Logout logic here

if __name__ == '__main__':
  
    app.run(debug=True)