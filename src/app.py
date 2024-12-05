from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)

    api = Api(app, doc="/swagger/")

    from routes.weather_routes import weather_bp

    api.add_namespace(weather_bp, path="/api/weather")

    return app
