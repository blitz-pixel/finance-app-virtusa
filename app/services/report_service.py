from app.models import Category, Expense
from app.extensions import db
from sqlalchemy import func, extract


def generate_report(user):
    try:
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

        return { "message" : "Data fetched successfully",
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
            "status_code": 200
        }
    
    except Exception as e:
        print(f"Error occurred while generating report: {e}")
        return {
            "message": "An error occurred",
            "monthly_totals": None,
            "yearly_totals": None,
            "monthly_category_totals": None,
            "yearly_category_totals": None,
            "status_code": 500
        }
    