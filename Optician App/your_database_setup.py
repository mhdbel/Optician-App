# your_database_setup.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model  # you can use this alias if you want, or just extend db.Model directly


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
