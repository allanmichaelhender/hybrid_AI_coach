import uuid
from sqlalchemy import String, Boolean, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.session import Base

class UserPlan(Base):
    __tablename__ = "user_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        index=True, 
        nullable=False)
    
    day_index: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Link to our Workout Library
    workout_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workouts.id"), nullable=True
    )
    
    # UI/Agent control: If True, AI Suggest won't touch this day
    is_user_locked: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationship to easily fetch workout details in one query
    workout = relationship("Workout")
