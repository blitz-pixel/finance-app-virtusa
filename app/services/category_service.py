from app.models import Category
from app.extensions import db
from datetime import datetime


def add_category(name, date, user):
    try:
        category_exists = Category.query.filter_by(name=name, user_id=user.user_id).first()
        if category_exists:
            return {
                "message": "Category already exists",
                "date": None,
                "category_id": None,
                "status_code": 400,
            }
        new_category = Category(name=name, date_added=date, user_id=user.user_id)
        db.session.add(new_category)
        db.session.flush()
        new_date = new_category.date_added
        category_id = new_category.category_id
        db.session.commit()
        return {
            "message": "Category added successfully",
            "date": new_date,
            "category_id": category_id,
            "status_code": 200,
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while adding category: {e}")
        return {
            "message": "An error occurred",
            "date": None,
            "category_id": None,
            "status_code": 500,
        }
    
def delete_category(category_id, user):
    try:
        deleted_rows = db.session.query(Category).filter(Category.category_id == category_id, Category.user_id == user.user_id).delete()
        if deleted_rows == 0:
            db.session.rollback()
            return {
                "message": "Category not found",
                "category_id": category_id,
                "status_code" : 404,
            }
        db.session.commit()
        return {
            "message": "Category deleted successfully",
            "category_id": category_id,
            "status_code": 200
        }
    except Exception as e:
            db.session.rollback()
            print(f"Error occurred while deleting category: {e}")
            return {
                "message": "An error occurred",
                "category_id": category_id,
                "status_code": 500
            }
    
def get_categories(user):
    try:
        categories = Category.query.filter_by(user_id=user.user_id).all()
        return {
            "message" : "Data fetched successfully",
            "categories": categories,
            "status_code": 200
        }
    except Exception as e:
        print(f"Error occurred while displaying categories: {e}")
        return {
            "message": "An error occurred",
            "categories": None,
            "status_code": 500
        }
