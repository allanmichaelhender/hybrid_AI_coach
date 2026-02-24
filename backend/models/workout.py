import uuid
from sqlalchemy import String, Float, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from database.base_class import Base

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    
    modality: Mapped[str] = mapped_column(String(50), index=True)
    focus: Mapped[str] = mapped_column(String(50), index=True)
    
    calculated_tss: Mapped[float] = mapped_column(Float)
    
    description: Mapped[str] = mapped_column(Text)
    
    structure: Mapped[list] = mapped_column(JSONB, nullable=False)
    
    embedding: Mapped[list[float]] = mapped_column(Vector(384))

    
    # Defining what happends when we print or log a workout
    def __repr__(self):
        return f"<Workout {self.title} ({self.modality})>"
