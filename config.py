import os

class Config:
    SECRET_KEY = 'your-secret-key'  # Replace with a secure secret key for Flask sessions and CSRF protection
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pizza.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-jwt-secret-key'  # Replace with a secure secret key for JWT encryption
