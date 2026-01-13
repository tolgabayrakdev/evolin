from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import event


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


@event.listens_for(Base, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    """Update updated_at timestamp before update."""
    target.updated_at = datetime.now(timezone.utc)


db = SQLAlchemy(model_class=Base)
