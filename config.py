import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base application configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretcampuskey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///campus_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
