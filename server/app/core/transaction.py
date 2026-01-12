import logging
from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


@contextmanager
def transaction(db: Session) -> Generator[Session, None, None]:
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Transaction error, rolling back: {e}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error in transaction, rolling back: {e}")
        db.rollback()
        raise


@contextmanager
def savepoint(db: Session) -> Generator[Session, None, None]:
    savepoint_obj = db.begin_nested()
    try:
        yield db
        savepoint_obj.commit()
    except SQLAlchemyError as e:
        logger.error(f"Savepoint error, rolling back: {e}")
        savepoint_obj.rollback()
        raise
