# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///optician_app.db'  # For production, use PostgreSQL/MySQL.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
