import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.environ.get(
        'JWT_SECRET_KEY',
        os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///evolin.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_ORIGINS = [
        "https://localhost:5173",
        "http://localhost:5173",
    ]
    CORS_SUPPORTS_CREDENTIALS = True