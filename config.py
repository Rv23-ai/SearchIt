import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base application configuration class."""
    # Ensure SECRET_KEY is strong and not using predictable default values
    env_secret = os.environ.get('SECRET_KEY')
    if not env_secret or env_secret == 'supersecretcampuskey':
        SECRET_KEY = secrets.token_hex(32)
    else:
        SECRET_KEY = env_secret

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///campus_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security & Session Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    WTF_CSRF_TIME_LIMIT = 3600

