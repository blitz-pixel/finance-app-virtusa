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
        print("\n--- INCOMING REQUEST DEBUG ---")
        print(f"Method: {request.method}")
        print(f"Headers: \n{request.headers}") # See if 'Content-Type' is missing
        print(f"Form Data: {request.form}")    # If data is here, your JS header is wrong
        print(f"Raw Body: {request.data}")      # Shows you exactly what JS sent
        print("-------------------------------\n")
        # data = request.get_json()
        # username  = data.get('username')
        # email = data.get('email')
        # password = data.get('password')
        # print(username,email,password)
        # hashed_password = generate_password_hash(password)
        # print(check_password_hash(hashed_password,password))
    
    return render_template('signup.html')
    # username = request.form.get('username')
    # email = request.form.get('email')
    # password = request.form.get('password')
    # new_user = User(user_name=username, email=email, password=password)
    # db.session.add(new_user)
    # db.session.commit()



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