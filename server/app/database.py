"""
Database configuration and session management.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .config.settings import settings

logger = logging.getLogger(__name__)

try:
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,  # Bağlantıyı kullanmadan önce kontrol eder
        pool_size=10,  # Connection pool size
        max_overflow=20,  # Maximum overflow connections
        connect_args={"connect_timeout": 5}  # 5 saniye timeout
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    engine = None
    SessionLocal = None


def get_db():
    if SessionLocal is None:
        raise ConnectionError("Database connection is not available")
    
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
