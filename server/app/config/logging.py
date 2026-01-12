"""
Logging configuration.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .settings import settings


def setup_logging():
    """
    Configure logging system.
    - Console output
    - File output (logs/app.log)
    - Error file output (logs/errors.log)
    - Log rotation (10MB, 5 backup files)
    - Format: timestamp, level, module, message
    """
    # Logs klasörünü oluştur (server dizini seviyesinde, app dışında)
    # Bu sayede uvicorn'un hot reload'u log dosyalarını izlemez
    log_dir = Path(settings.log_dir)
    if not log_dir.is_absolute():
        # Relative path ise, server dizini seviyesinde oluştur
        # app/main.py'den 2 seviye yukarı çık (app -> server)
        base_dir = Path(__file__).parent.parent.parent
        log_dir = base_dir / settings.log_dir
    log_dir.mkdir(exist_ok=True)

    # Log formatı
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Root logger'ı yapılandır
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Mevcut handler'ları temizle (tekrar yapılandırma durumunda)
    root_logger.handlers.clear()

    # Console Handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    # File Handler (app.log) - Rotating
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 5 backup dosya
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    # Error Handler (errors.log) - Sadece ERROR ve CRITICAL
    error_handler = RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 5 backup dosya
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)

    # SQLAlchemy loglarını azalt (çok verbose)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return root_logger
