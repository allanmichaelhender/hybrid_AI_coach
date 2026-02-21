from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base_class import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

