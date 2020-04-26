from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    with app.app_context():
        from app import routes

        from .dashboards import template_dashboard
        template_dashboard.add_dash(app)

        return app
