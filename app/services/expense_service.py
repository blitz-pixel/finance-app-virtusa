from app.models import Category, Expense
from app.extensions import db
from app.services.category_service import get_categories
from datetime import datetime

def add_expense(amount, date, description, category, user):
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return {
            "message" : "Amount must be a valid number",
            "date": None,
            "transaction_id": None,
            "status_code" : 400,
        }
    if int(amount) < 0:
        return {"message": "Amount cannot be negative", "date": None, "transaction_id": None, "status_code": 400}
    
    elif int(amount) > 999999999:
        return {"message": "Amount exceeds maximum limit", "date": None, "transaction_id": None, "status_code": 400}
    chosen_category = Category.query.filter_by(name=category, user_id=user.user_id).first()
    if not chosen_category:
        return {
            "message": "Category not found",
            "date": None,
            "transaction_id": None,
            "status_code": 404
        }

    new_expense = Expense(
        category_id=chosen_category.category_id,
        amount=amount,
        date=date,
        description=description,
        user_id=user.user_id
    )
    try:
        db.session.add(new_expense)
        db.session.flush()
        new_date = new_expense.date
        transaction_id = new_expense.transaction_id
        db.session.commit()
        return {
            "message": "Expense added successfully",
            "date": new_date,
            "transaction_id": transaction_id,
            "status_code": 200
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while adding expense: {e}")
        return {
            "message": "An error occurred",
            "date": None,
            "transaction_id": None,
            "status_code": 500
        }

def delete_expense(expense_id, current_user):
    try:
        deleted_row = db.session.query(Expense).filter(Expense.transaction_id == expense_id, Expense.user_id == current_user.user_id).delete()
        if deleted_row == 0:
            db.session.rollback()
            return {
                "message" : "Expense not found",
                "status_code" : 404
            }
        db.session.commit()
        return {
            "message": "Expense deleted successfully",
            "status_code": 200
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while deleting expense: {e}")
        return {
            "message": "An error occurred",
            "status_code": 500
        }

def load_expenses_and_categories(user):
    try:
        category_result = get_categories(user)
        if category_result["status_code"] != 200:
            return {
                "message": category_result["message"],
                "categories": None,
                "expenses": None,
                "status_code": category_result["status_code"]
            }
        categories = category_result["categories"]
        expenses = Expense.query.filter_by(user_id=user.user_id).all()
        return {
            "message": "Data fetched successfully",
            "categories": categories,
            "expenses": expenses,
            "status_code": 200
        }
    except Exception as e:
        print(f"Error occurred while displaying categories or expenses: {e}")
        return {
            "message": "An error occurred",
            "expenses": None,
            "categories": None,
            "status_code": 500
        }