from flask import Blueprint, render_template, url_for, redirect, jsonify, request, session
from sqlalchemy import func, extract
from app.extensions import db
from app.models import User, Category, Expense
from app.services.category_service import get_categories
from app.services.report_service import generate_report
from app.utils.decorators import login_required


route_bp = Blueprint("report", __name__)
@route_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report(user):        
        try: 
            category_result = get_categories(user)
            if category_result["status_code"] != 200:
                return jsonify({"message": category_result["message"]}), category_result["status_code"]
            all_categories = category_result["categories"] or []
            categories = [
                category.name
                for category in all_categories
            ]
        except Exception as e:
            print(f"Error occurred while fetching categories: {e}")
            return jsonify({"message": "An error occurred"}), 500

        if request.method == 'POST':
            try:
                result = generate_report(user)
            except Exception as e:
                print(f"Error occurred while generating report: {e}")
                return jsonify({"message": "An error occurred"}), 500
            return jsonify({
                "message": "Report generated successfully",
                "monthly_totals" : result["monthly_totals"],
                "yearly_totals" : result["yearly_totals"],
                "monthly_category_totals" : result["monthly_category_totals"],
                "yearly_category_totals" : result["yearly_category_totals"]
                }), result["status_code"]

        return render_template('report.html', categories=categories)

   