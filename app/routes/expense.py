from flask import Blueprint, render_template, url_for, redirect, jsonify, request, session

from app.extensions import db
from app.models import User, Category, Expense
from app.services.expense_service import add_expense,  delete_expense, load_expenses_and_categories
from app.utils.decorators import login_required

expense_bp = Blueprint("expense", __name__)

@expense_bp.route('/expense',methods=['GET', 'POST','DELETE'])
@login_required
def expense(user):
    username = user.user_name 
    if request.method == 'POST':
        try:
            data = request.get_json()
            category = data["category"]
            amount = data["amount"]
            date = data["date"] or db.func.current_date()
            description = data["description"]        
            result = add_expense(amount, date, description, category, user)
            return jsonify({"message": result["message"], "date": result["date"], "transaction_id": result["transaction_id"]}), result["status_code"]
        
        except Exception as e:
            print(f"Error occurred while adding expense: {e}")
            return jsonify({"message": "An error occurred"}), 500

    elif request.method == 'DELETE':
        try:
            expense_id = request.args["expense_id"]
            result = delete_expense(expense_id,user)
            return jsonify({"message": result["message"]}), result["status_code"]
        except Exception as e:
            print(f"Error occurred while deleting expense: {e}")
            return jsonify({"message": "An error occurred"}), 500
       
    
    try:
        result = load_expenses_and_categories(user)
        categories = result["categories"]
        expenses = result["expenses"]
    except Exception as e:
        return jsonify({"message": result["message"]}), result["status_code"]
    # print(categories)
    return render_template('expense.html',categories=categories, expenses=expenses, username=username)
