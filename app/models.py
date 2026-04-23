from .extensions import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            "email": self.email,
            "user_name": self.user_name,
            "created_at": self.created_at,
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
            "name": self.name,
            "date_added": self.date_added,
        }


class Expense(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    date = db.Column(db.Date, nullable=False, server_default=db.func.current_date())
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.category_id'), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)
