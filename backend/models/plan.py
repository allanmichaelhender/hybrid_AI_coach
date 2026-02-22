import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB # 👈 Essential for the AI block
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.session import Base

class UserPlan(Base):
    __tablename__ = "user_plans"

    # 1. Identity
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        index=True, 
        nullable=False
    )
    
    # 2. Metadata (What the endpoint is sending)
    plan_name: Mapped[str] = mapped_column(String, nullable=True)
    user_goal: Mapped[str] = mapped_column(String, nullable=False)
    
    # 3. The Payload (The 14-day JSON array from React)
    # This stores your 'synthetic' workouts and 'workout_id's in one blob
    calendar_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    
    # 4. The AI Reasoning
    coach_reasoning: Mapped[str] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship("User", back_populates="plans")
