import uuid
from sqlalchemy import String, Integer, Float, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from database.session import Base

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Store Enums as strings in DB for easier migrations
    modality: Mapped[str] = mapped_column(String(50), index=True)
    focus: Mapped[str] = mapped_column(String(50), index=True)
    
    rpe: Mapped[int] = mapped_column(Integer)
    calculated_tss: Mapped[float] = mapped_column(Float)
    
    description: Mapped[str] = mapped_column(Text)
    
    # The 'Contract': Nested interval data stored as JSON
    # e.g. [{"name": "Warmup", "repeat_count": 1, "steps": [...]}]
    structure: Mapped[list] = mapped_column(JSONB, nullable=False)
    
    # pgvector column for Hugging Face all-MiniLM-L6-v2 (384 dims)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))

    def __repr__(self):
        return f"<Workout {self.title} ({self.modality})>"
