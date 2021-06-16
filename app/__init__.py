import logging

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig
from control.config import ProductionConfig

db = SQLAlchemy()
nav = Nav()


def create_app():
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config.from_object(ProductionConfig)

    # logg_handler = logging.FileHandler("app.log")
    logging.basicConfig(filename="app.log", level=logging.INFO)
    # logg_handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    # app.logger.addHandler(logg_handler)

    # Initialise the application database
    db.init_app(app)

    Bootstrap(app)

    @nav.navigation()
    def nav_bar():
        return Navbar(
            View("Home", "home.home_page"),
            # Link('Descriptive Text', dest='https://www.url.com/'),
            View("Admin Console", "admin.index"),
            View(f"{current_user.email}", endpoint="home.home_page"),
            # View('Register', 'security.register'),
            View("Products Home", "products.list_all_products"),
            View("Register New Product", "products.add_product"),
            View("Analytics", "analytics.total_sales_by", key="department"),
            View("Log Out", "security.logout"),
        )

    nav.init_app(app)

    @app.before_first_request
    def add_user():
        # from app.models import UserSesan
        user1 = User(email="xyz@yahoo.com", password=hash_password("password"))
        user2 = User(
            email="wale.adekoya@btinternet.com", password=hash_password("password")
        )
        if all(
            [
                (User.query.filter(User.email == "xyz@yahoo.com").first() is None),
                (
                    User.query.filter(
                        User.email == "wale.adekoya@btinternet.com"
                    ).first()
                    is None
                ),
            ]
        ):
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    with app.app_context():
        # import the models after initialising the db object
        from .models.models import User, Role, ProductCategory, Product
        from app.routes.home import HomePageFromAdmin

        # Setup Flask-Security
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(app, user_datastore)

        db.create_all()
        db.session.commit()

        from .routes.home import home
        from .routes.product_view import product
        from .routes.analytics import analytics

        # from .routes.login_view import login

        # registering blueprints
        app.register_blueprint(home)
        app.register_blueprint(product)
        app.register_blueprint(analytics)

        admin = Admin(app, template_mode="bootstrap4")
        admin.add_view(ModelView(User, db.session))
        admin.add_view(ModelView(Role, db.session))
        admin.add_view(ModelView(ProductCategory, db.session))
        admin.add_view(ModelView(Product, db.session))

        # add custom views
        admin.add_view(
            HomePageFromAdmin(name="Back To Main Page", endpoint="home.home_page")
        )

    return app
