from flask import Blueprint, render_template, url_for, redirect, jsonify, request, session

from app.extensions import db
from app.models import User, Category
from app.services.category_service import add_category, delete_category, get_categories
from app.utils.decorators import login_required


category_bp = Blueprint("category", __name__)


@category_bp.route('/category', methods=['GET', 'POST', 'DELETE'])
@login_required
def category(user):
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON data"}), 400
        name = data.get('name')
        date = data.get('date') or db.func.current_date()
        
        result = add_category(name, date, user)
        return jsonify({"message": result["message"], "date": result.get("date"), "category_id": result.get("category_id")}), result["status_code"]
    elif request.method == 'DELETE':
        category_id = request.args.get('category_id')
        if not category_id:
            return jsonify({"message": "category_id is required"}), 400
        result = delete_category(category_id, user)
        return jsonify({"message": result["message"]}), result["status_code"]
    
    try:
        result = get_categories(user)
        if result["status_code"] != 200:
            return jsonify({"message": result["message"]}), result["status_code"]
        categories = result["categories"]
    except Exception as e:
        print(f"Error occurred while displaying categories: {e}")
        return jsonify({"message": "An error occurred"}), 500

    return render_template('category.html',categories=categories)