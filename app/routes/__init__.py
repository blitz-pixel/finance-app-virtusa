from .auth import auth_bp
from .expense import expense_bp
from .report import route_bp
from .main import home_bp
from .category import category_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(route_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(category_bp)